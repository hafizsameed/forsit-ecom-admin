import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_db
from app.models.models import Category, Product
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root(setup_database):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "E-commerce Admin Dashboard API"


def test_create_category(setup_database):
    category_data = {"name": "Test Category", "description": "Test Description"}
    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["description"] == category_data["description"]
    assert "id" in data


def test_create_product(setup_database):
    category_data = {"name": "Electronics", "description": "Electronic devices"}
    category_response = client.post("/api/v1/categories/", json=category_data)
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "sku": "TEST-001",
        "price": 99.99,
        "category_id": category_id,
    }

    product_response = client.post("/api/v1/products/", json=product_data)
    assert product_response.status_code == 201
    data = product_response.json()
    assert data["name"] == product_data["name"]
    assert data["sku"] == product_data["sku"]
    assert data["category"]["id"] == category_id
