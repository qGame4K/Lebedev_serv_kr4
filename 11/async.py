import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from faker import Faker
from task_11.main_app import app, db

fake = Faker() # [cite: 134, 135]

@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    # Изоляция состояния [cite: 136, 137]
    db.clear()
    yield
    db.clear()

@pytest_asyncio.fixture
async def async_client():
    # Настройка клиента без реального сервера [cite: 132, 133]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_user_async(async_client):
    data = {"username": fake.name(), "age": fake.random_int(min=18, max=80)} # [cite: 134]
    response = await async_client.post("/users", json=data)
    assert response.status_code == 201 # [cite: 127]
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_existing_user(async_client):
    data = {"username": fake.name(), "age": 25}
    create_res = await async_client.post("/users", json=data)
    user_id = create_res.json()["id"]

    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200 # [cite: 128]
    assert response.json()["username"] == data["username"]

@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client):
    response = await async_client.get("/users/9999")
    assert response.status_code == 404 # [cite: 129]

@pytest.mark.asyncio
async def test_delete_existing_user(async_client):
    create_res = await async_client.post("/users", json={"username": fake.name(), "age": 30})
    user_id = create_res.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")
    assert response.status_code == 204 # [cite: 130]

@pytest.mark.asyncio
async def test_delete_nonexistent_user(async_client):
    response = await async_client.delete("/users/9999")
    assert response.status_code == 404 # [cite: 131]