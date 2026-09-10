import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# En local, on pointe vers le Postgres lancé par docker-compose (port publié sur ta machine).
# En CI, cette variable sera fournie par le workflow GitHub Actions (on verra ça juste après).
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://todo_user:todo_password@localhost:5432/todo_db",
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Buy milk", "description": "2 liters"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False


def test_list_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/tasks", json={"title": "Old title"})
    task_id = created.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    created = client.post("/tasks", json={"title": "To delete"})
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404