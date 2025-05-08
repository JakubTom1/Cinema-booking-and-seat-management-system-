# test_user.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Importuj główną aplikację FastAPI
from backend.database import SessionLocal, Base, engine
from backend.models import User
from sqlalchemy.orm import Session
from backend.database import get_db

# Tworzymy bazę danych testową na potrzeby testów
@pytest.fixture(scope="function")
def db():
    """
    Fixture dostarczająca instancję sesji bazy danych na potrzeby testów.
    """
    db_generator = get_db()
    db = next(db_generator)  # Pobranie instancji sesji z generatora
    try:
        yield db
    finally:
        db.close()


# Używamy TestClient do testowania endpointów
@pytest.fixture
def client():
    from backend.main import app  # Assuming your FastAPI app is in app.main
    with TestClient(app) as client:
        yield client


# Testowanie endpointu logowania
def test_login(client: TestClient, db: Session):
    # Tworzenie użytkownika
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "password",
        "status": 0
    }
    user = User(**user_data)
    db.add(user)
    db.commit()

    # Wykonujemy zapytanie logowania
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "password"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


# Testowanie endpointu tworzenia użytkownika
def test_create_user(client: TestClient, db: Session):
    # Sprawdzanie, czy użytkownik już nie istnieje
    response = client.post(
        "/users/",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "login": "alice",
            "password": "alicepassword",
            "status": 1
        }
    )

    # Sprawdzamy, czy użytkownik został utworzony
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["first_name"] == "Alice"
    assert response_data["login"] == "alice"

    # Sprawdzamy, czy użytkownik pojawił się w bazie
    db_user = db.query(User).filter(User.login == "alice").first()
    assert db_user is not None
    assert db_user.first_name == "Alice"


# Testowanie endpointu dostępu do użytkownika po loginie (z autoryzacją)
def test_get_user(client: TestClient, db: Session):
    # Tworzymy użytkownika
    user_data = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "login": "charlie",
        "password": "charliepassword",
        "status": 1
    }
    user = User(**user_data)
    db.add(user)
    db.commit()

    # Wykonanie logowania
    login_response = client.post(
        "/token",
        data={"username": "charlie", "password": "charliepassword"}
    )
    token = login_response.json().get("access_token")

    # Dostęp do użytkownika z tokenem
    response = client.get(
        "/users/charlie",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["login"] == "charlie"
    assert response.json()["first_name"] == "Charlie"


# Testowanie nieautoryzowanego dostępu (brak tokenu)
def test_unauthorized_access(client: TestClient):
    response = client.get("/users/charlie")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
