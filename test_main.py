# test_main.py
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


def test_create_item(client):
    response = client.post(
        "/items/", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
