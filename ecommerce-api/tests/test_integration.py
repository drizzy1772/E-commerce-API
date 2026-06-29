

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

TEST_USER = {
    "email": "testuser@example.com",
    "password": "testpass123"
}

TEST_PRODUCT = {
    "name": "Wireless keyboard",
    "price": 26.01,
    "stock": 10
}



response = client.post("/auth/register", json=TEST_USER)
assert response.status_code == 200


response = client.post(
        "/auth/login",
        json={
            "username": TEST_USER["email"],
            "password": TEST_USER["password"],
        },
    )

assert response.status_code == 200
    
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

response = client.post("/products", json=TEST_PRODUCT, headers=headers)
assert response.status_code == 200

product_id = response.json()["id"]

response = client.post(
        "/cart/add",
        json={
            "product_id": product_id,
            "quantity": 1,
        },
        headers=headers,
    )
assert response.status_code == 200

body = response.json()
assert body['product_id'] == product_id
assert body['quantity'] == 1

response = client.post(
    "/orders",
    headers=headers
)
assert response.status_code == 200

order_id = response.json()["id"]

response = client.get(
    f"/orders/{order_id}",
    headers=headers,
)
assert response.status_code == 200

exist_order = response.json()

assert exist_order["id"] == order_id
assert len(exist_order["items"]) == 1
assert exist_order["items"][0]["product_id"] == product_id
assert exist_order["items"][0]["quantity"] == 1