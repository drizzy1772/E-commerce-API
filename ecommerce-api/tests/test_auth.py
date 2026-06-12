
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)




def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser1@1test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    print(response.json())
    assert "email" in response.json()

    
    
def test_register_duplicate():
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser1@test.com",
            "password": "password123",
        },
    )
    
    assert response.status_code == 400
    
def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "newuser1@test.com",
            "password": "password123"
        }
    )
    print(response.json())
    assert response.status_code == 200
    
    assert "access_token" in response.json()
    