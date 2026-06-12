




from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200

def test_get_products_with_filters():
    response = client.get("/products/?min_price=100")
    assert response.status_code == 200
    
    products = response.json()
    
    for product in products:
        assert product["price"] >= 100
