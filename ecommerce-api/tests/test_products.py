




from fastapi.testclient import TestClient
from app.main import app


def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200

def test_get_products_with_filters(client):
    response = client.get("/products/?min_price=100")
    assert response.status_code == 200
    
    products = response.json()
    
    for product in products:
        assert product["price"] >= 100
