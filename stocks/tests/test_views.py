
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey
from unittest.mock import patch

@pytest.mark.django_db
def test_user_signup():
    client = APIClient()
    data = {
        "username": "testuser",
        "password": "password123",
        "email": "testuser@example.com"
    }
    response = client.post("/api/signup/", data, format='json')
    assert response.status_code == 201
    assert "api_key" in response.data
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_user_signup_missing_fields():
    client = APIClient()
    data = {
        "username": "testuser"
    }
    response = client.post("/api/signup/", data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_login():
    user = User.objects.create_user(username="testuser", password="password123")
    client = APIClient()
    data = {
        "username": "testuser",
        "password": "password123"
    }
    response = client.post("/api/login/", data, format='json')
    assert response.status_code == 200
    assert "api_key" in response.data

@pytest.mark.django_db
def test_user_login_invalid_credentials():
    client = APIClient()
    data = {
        "username": "invaliduser",
        "password": "password123"
    }
    response = client.post("/api/login/", data, format='json')
    assert response.status_code == 400

