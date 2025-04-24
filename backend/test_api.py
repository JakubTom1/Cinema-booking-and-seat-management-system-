import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pytest
from fastapi.testclient import TestClient
import json
from main import app
from database import get_db, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_movies(test_db):
    response = client.get("/movies/{--placeholder--}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_login(test_db):
    data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/token", data=data)
    assert response.status_code in [200, 401]
if __name__ == "__main__":
    test_db()