import os
import tempfile
import pytest

from app import app

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Inventory Management API is running"


def test_create_item(client):
    response = client.post(
        "/items",
        json={
            "name": "Test Milk",
            "category": "Dairy",
            "price": 100,
            "quantity": 10,
            "barcode": "TEST001"
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test Milk"
    assert response.json["price"] == 100


def test_get_items(client):
    client.post(
        "/items",
        json={
            "name": "Test Bread",
            "category": "Bakery",
            "price": 80,
            "quantity": 5,
            "barcode": "TEST002"
        }
    )

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Test Bread"


def test_get_single_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Test Rice",
            "category": "Grains",
            "price": 200,
            "quantity": 20,
            "barcode": "TEST003"
        }
    )

    item_id = create_response.json["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json["name"] == "Test Rice"


def test_update_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Test Sugar",
            "category": "Grocery",
            "price": 150,
            "quantity": 10,
            "barcode": "TEST004"
        }
    )

    item_id = create_response.json["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={
            "price": 175
        }
    )

    assert response.status_code == 200
    assert response.json["price"] == 175


def test_delete_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Test Juice",
            "category": "Beverages",
            "price": 120,
            "quantity": 8,
            "barcode": "TEST005"
        }
    )

    item_id = create_response.json["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 200

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 404
