import pytest
from rest_framework.test import APIClient


# registration tests
@pytest.mark.django_db
def test_user_registration_success():
    client = APIClient()
    payload = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "customer"
    }

    response = client.post("/api/v1/register/", payload)

    assert response.status_code == 201
    assert "message" in response.data
    assert "Successfully Registered" in response.data["message"]

@pytest.mark.django_db
def test_user_registration_failure_1():
    client = APIClient()
    payload = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "admin"
    }

    response = client.post("/api/v1/register/", payload)

    assert response.status_code == 400

@pytest.mark.django_db
def test_user_registration_failure_2():
    client = APIClient()
    user1 = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "customer"
    }

    response = client.post("/api/v1/register/", user1)
    user2 = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "restaurant_admin"
    }
    response = client.post("/api/v1/register/", user2)
    assert response.status_code == 400



# Login tests
@pytest.mark.django_db
def test_user_login_success():
    client = APIClient()

    register = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "customer"
    }

    response = client.post("/api/v1/register/", register)

    login = {
        "email": "customer10@example.com",
        "password": "123"
    }

    response = client.post("/api/v1/login/", login)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_login_failure():
    client = APIClient()

    register = {
        "email": "customer10@example.com",
        "password": "123",
        "user_type": "customer"
    }

    response = client.post("/api/v1/register/", register)

    login = {
        "email": "customer10@example.com",
        "password": "1234" # Incorrect password
    }

    response = client.post("/api/v1/login/", login)

    assert response.status_code == 401
    