

from app.main import app
from fastapi.testclient import TestClient
import asyncio
from tests.conftest import TestingSessionLocal
from app.models.models import Product, Category


client = TestClient(app)

TEST_USER = {
    "email": "testuser@example.com",
    "password": "Testpass123"
}

def test_full_flow(client):

    async def seed():
        async with TestingSessionLocal() as db:
            category = Category(
                name="Electronics",
                slug="electronics"
            )
            db.add(category)
            await db.commit()
            await db.refresh(category)
            product = Product(
                name="Wireless keyboard",
                description="good keyboard",
                price=26.11,
                stock=8,
                category_id=category.id
            )
            db.add(product)
            await db.commit()
            await db.refresh(product)
            return product.id

    product_id = asyncio.get_event_loop().run_until_complete(seed())
    response = client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 200


    response = client.post(
            "/auth/login",
            data={
                "username": TEST_USER["email"],
                "password": TEST_USER["password"],
            },
        )

    assert response.status_code == 200
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    response = client.post(
            "/cart/items",
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
        "/orders/",
        headers=headers
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.get(
        f"/orders/{order_id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == order_id