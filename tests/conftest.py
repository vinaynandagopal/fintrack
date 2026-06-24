import os
import sys
import uuid

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

from app import create_app


def unique_email():
    return f"test_{uuid.uuid4().hex[:10]}@example.com"


def register_user(client):
    payload = {
        "full_name": "Test User",
        "email": unique_email(),
        "password": "password123"
    }

    response = client.post("/api/auth/register", json=payload)
    data = response.get_json()

    return response, data, payload


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


import pytest


@pytest.fixture()
def app():
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True
    })
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()