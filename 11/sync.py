from fastapi.testclient import TestClient
from task_11.main_app import app, db
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    db.clear()
    yield
    db.clear()

def test_create_user_sync():
    response = client.post("/users", json={"username": "Alice", "age": 25})
    assert response.status_code == 201
    assert response.json()["username"] == "Alice"

def test_get_user_sync():
    res_post = client.post("/users", json={"username": "Bob", "age": 30})
    user_id = res_post.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "Bob"

def test_delete_user_sync():
    res_post = client.post("/users", json={"username": "Charlie", "age": 35})
    user_id = res_post.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    response_check = client.get(f"/users/{user_id}")
    assert response_check.status_code == 404