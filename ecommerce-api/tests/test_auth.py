
from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)

TEST_EMAIL = email = f"testuser_{uuid.uuid4().hex[:8]}@test.com"
TEST_PASSWORD = "Password123"


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200
    print(response.json())
    assert "email" in response.json()

    
    
def test_register_duplicate():
    response = client.post(
        "/auth/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )
    
    assert response.status_code == 400
    
def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    print(response.json())
    assert response.status_code == 200
    
    assert "access_token" in response.json()