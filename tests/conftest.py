import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False,
                      "SQLALCHEMY_DATABASE_URI": "sqlite://", "SECRET_KEY": "test"})
    return app.test_client()


@pytest.fixture()
def signup():
    def _signup(client, email="a@example.com", password="password123"):
        return client.post("/register", data={"email": email, "password": password, "confirm": password})
    return _signup
