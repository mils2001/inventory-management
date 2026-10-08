from unittest.mock import Mock


def test_search_products(client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Test Milk",
                "code": "123456",
                "brands": "Test Brand",
                "categories": "Dairy"
            }
        ]
    }

    monkeypatch.setattr(
        "app.requests.get",
        lambda *args, **kwargs: mock_response
    )

    response = client.get("/products/search?name=milk")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Test Milk"
    assert response.json[0]["barcode"] == "123456"
    assert response.json[0]["brand"] == "Test Brand"


def test_get_product_by_barcode(client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Chocolate Milk",
            "brands": "Test Brand",
            "categories": "Dairy",
            "quantity": "500 ml",
            "image_url": "https://example.com/image.jpg"
        }
    }

    monkeypatch.setattr(
        "app.requests.get",
        lambda *args, **kwargs: mock_response
    )

    response = client.get("/products/barcode/123456")

    assert response.status_code == 200
    assert response.json["name"] == "Test Chocolate Milk"
    assert response.json["barcode"] == "123456"
    assert response.json["brand"] == "Test Brand"
    assert response.json["category"] == "Dairy"
    assert response.json["quantity"] == "500 ml"


def test_import_product(client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Imported Milk",
            "categories": "Dairy"
        }
    }

    monkeypatch.setattr(
        "app.requests.get",
        lambda *args, **kwargs: mock_response
    )

    response = client.post(
        "/products/import",
        json={
            "barcode": "789012",
            "price": 120,
            "quantity": 10
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "Imported Milk"
    assert response.json["category"] == "Dairy"
    assert response.json["price"] == 120
    assert response.json["quantity"] == 10
    assert response.json["barcode"] == "789012"


def test_search_products_requires_name(client):
    response = client.get("/products/search")

    assert response.status_code == 400
    assert response.json["error"] == "Product name is required"


def test_product_barcode_not_found(client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 0
    }

    monkeypatch.setattr(
        "app.requests.get",
        lambda *args, **kwargs: mock_response
    )

    response = client.get("/products/barcode/999999")

    assert response.status_code == 404
    assert response.json["error"] == "Product not found"
