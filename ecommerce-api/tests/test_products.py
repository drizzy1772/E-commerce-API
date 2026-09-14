




from fastapi.testclient import TestClient
from app.main import app


def test_get_products(client):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200

def test_get_products_with_filters(client):
    response = client.get("/api/v1/products/?min_price=100")
    assert response.status_code == 200
    
    data = response.json()
    
    for product in data["items"]:
        assert product["price"] >= 100
