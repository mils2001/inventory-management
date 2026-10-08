from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

DATABASE = "inventory.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management API is running"})


@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()

    return jsonify([dict(item) for item in items])


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    conn = get_db()

    item = conn.execute(
        "SELECT * FROM items WHERE id = ?",
        (item_id,)
    ).fetchone()

    conn.close()

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(dict(item))


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "name",
        "category",
        "price",
        "quantity",
        "barcode"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO items
            (name, category, price, quantity, barcode)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["category"],
                data["price"],
                data["quantity"],
                data["barcode"]
            )
        )

        conn.commit()

        item = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify(dict(item)), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Barcode already exists"}), 409

    finally:
        conn.close()


@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    allowed_fields = [
        "name",
        "category",
        "price",
        "quantity",
        "barcode"
    ]

    updates = []
    values = []

    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            values.append(data[field])

    if not updates:
        return jsonify({"error": "No valid fields provided"}), 400

    values.append(item_id)

    conn = get_db()

    try:
        cursor = conn.execute(
            f"""
            UPDATE items
            SET {", ".join(updates)}
            WHERE id = ?
            """,
            values
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404

        item = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

        return jsonify(dict(item))

    except sqlite3.IntegrityError:
        return jsonify({"error": "Barcode already exists"}), 409

    finally:
        conn.close()


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM items WHERE id = ?",
        (item_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted successfully"})


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
            return jsonify({
                "error": "External API request failed"
            }), 502

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
        return jsonify({
            "error": "Unable to connect to external API"
        }), 502


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
            return jsonify({
                "error": "External API request failed"
            }), 502

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
        return jsonify({
            "error": "Unable to connect to external API"
        }), 502


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
            return jsonify({
                "error": "External API request failed"
            }), 502

        result = response.json()

        if result.get("status") != 1:
            return jsonify({"error": "Product not found"}), 404

        product = result.get("product", {})

        conn = get_db()

        cursor = conn.execute(
            """
            INSERT INTO items
            (name, category, price, quantity, barcode)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                product.get("product_name") or "Unknown Product",
                product.get("categories") or "Uncategorized",
                data.get("price", 0),
                data.get("quantity", 0),
                barcode
            )
        )

        conn.commit()

        item = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        conn.close()

        return jsonify(dict(item)), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Barcode already exists"}), 409

    except requests.RequestException:
        return jsonify({
            "error": "Unable to connect to external API"
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
