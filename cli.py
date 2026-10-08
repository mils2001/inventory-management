
import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/items")
    print(response.json())


def add_item():
    name = input("Name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))
    barcode = input("Barcode: ")

    data = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "barcode": barcode
    }

    response = requests.post(f"{BASE_URL}/items", json=data)
    print(response.json())


def update_item():
    item_id = int(input("Item ID: "))
    field = input("Field to update: ")
    value = input("New value: ")

    if field in ["price"]:
        value = float(value)
    elif field in ["quantity"]:
        value = int(value)

    response = requests.patch(
        f"{BASE_URL}/items/{item_id}",
        json={field: value}
    )

    print(response.json())


def delete_item():
    item_id = int(input("Item ID: "))

    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print(response.json())


def search_product():
    name = input("Product name: ")

    response = requests.get(
        f"{BASE_URL}/products/search",
        params={"name": name}
    )

    print(response.json())


def import_product():
    barcode = input("Product barcode: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))

    data = {
        "barcode": barcode,
        "price": price,
        "quantity": quantity
    }

    response = requests.post(
        f"{BASE_URL}/products/import",
        json=data
    )

    print(response.json())


def menu():
    while True:
        print("\nInventory Management CLI")
        print("1. View inventory")
        print("2. Add item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Search OpenFoodFacts")
        print("6. Import product")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            search_product()
        elif choice == "6":
            import_product()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()

