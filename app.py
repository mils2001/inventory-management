from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "name": "Milk",
        "category": "Dairy",
        "price": 120.00,
        "quantity": 20,
        "barcode": "6001001001001"
    },
    {
        "id": 2,
        "name": "Bread",
        "category": "Bakery",
        "price": 80.00,
        "quantity": 15,
        "barcode": "6001001001002"
    },
    {
        "id": 3,
        "name": "Apple Juice",
        "category": "Beverages",
        "price": 150.00,
        "quantity": 10,
        "barcode": "6001001001003"
    }
]


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management API is running"})


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(inventory)


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "category", "price", "quantity", "barcode"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    item = {
        "id": max([item["id"] for item in inventory], default=0) + 1,
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "quantity": data["quantity"],
        "barcode": data["barcode"]
    }

    inventory.append(item)

    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for item in inventory:
        if item["id"] == item_id:
            for field in ["name", "category", "price", "quantity", "barcode"]:
                if field in data:
                    item[field] = data[field]

            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Item deleted successfully"})

    return jsonify({"error": "Item not found"}), 404


@app.route("/products/search", methods=["GET"])
def search_products():
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "Product name is required"}), 400

    try:
        response = requests.get(
            "https://world.openfoodfacts.org/api/v2/search",
            params={
                "categories_tags": name,
                "page_size": 10,
                "fields": "code,product_name,brands,categories"
            },
            headers={
                "User-Agent": "InventoryManagementAPI/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": "External API request failed"}), 502

        data = response.json()

        products = []

        for product in data.get("products", []):
            products.append({
                "name": product.get("product_name"),
                "barcode": product.get("code"),
                "brand": product.get("brands"),
                "category": product.get("categories")
            })

        return jsonify(products)

    except requests.RequestException:
        return jsonify({"error": "Unable to connect to external API"}), 502


@app.route("/products/barcode/<barcode>", methods=["GET"])
def get_product_by_barcode(barcode):
    try:
        response = requests.get(
            f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
            headers={
                "User-Agent": "InventoryManagementAPI/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": "External API request failed"}), 502

        data = response.json()

        if data.get("status") != 1:
            return jsonify({"error": "Product not found"}), 404

        product = data.get("product", {})

        return jsonify({
            "name": product.get("product_name"),
            "barcode": barcode,
            "brand": product.get("brands"),
            "category": product.get("categories"),
            "quantity": product.get("quantity"),
            "image": product.get("image_url")
        })

    except requests.RequestException:
        return jsonify({"error": "Unable to connect to external API"}), 502


@app.route("/products/import", methods=["POST"])
def import_product():
    data = request.get_json()

    if not data or "barcode" not in data:
        return jsonify({"error": "Barcode is required"}), 400

    barcode = data["barcode"]

    try:
        response = requests.get(
            f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
            headers={
                "User-Agent": "InventoryManagementAPI/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": "External API request failed"}), 502

        result = response.json()

        if result.get("status") != 1:
            return jsonify({"error": "Product not found"}), 404

        product = result.get("product", {})

        item = {
            "id": max([item["id"] for item in inventory], default=0) + 1,
            "name": product.get("product_name") or "Unknown Product",
            "category": product.get("categories") or "Uncategorized",
            "price": data.get("price", 0),
            "quantity": data.get("quantity", 0),
            "barcode": barcode
        }

        inventory.append(item)

        return jsonify(item), 201

    except requests.RequestException:
        return jsonify({"error": "Unable to connect to external API"}), 502


if __name__ == "__main__":
    app.run(debug=True)
