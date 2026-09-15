import pytest

import database
import repository
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_api.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_db
    )

    database.create_tables()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_api_home(client):
    response = client.get("/api")

    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Afaq Foundation API is running."
    )


def test_register(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Afaq Member",
            "email": "member@afaq.org",
            "password": "secret123"
        }
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["user"]["email"] == "member@afaq.org"

    # Password hashes must NEVER be returned
    assert "password_hash" not in data["user"]


def test_login(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Afaq Member",
            "email": "member@afaq.org",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "member@afaq.org",
            "password": "secret123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["user"]["role"] == "member"
    assert "password_hash" not in data["user"]


def test_wrong_login(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Afaq Member",
            "email": "member@afaq.org",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "member@afaq.org",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_create_project(client):
    response = client.post(
        "/api/projects",
        json={
            "title": "Education Without Barriers",
            "description": "Supporting education.",
            "category": "Education",
            "location": "Kenya",
            "target_amount": 100000
        }
    )

    assert response.status_code == 201

    project = response.get_json()

    assert project["title"] == (
        "Education Without Barriers"
    )

    assert project["amount_raised"] == 0.0


def test_get_projects(client):
    repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    response = client.get("/api/projects")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_missing_project(client):
    response = client.get("/api/projects/999")

    assert response.status_code == 404


def test_api_donation_updates_project(client):
    user_response = client.post(
        "/api/auth/register",
        json={
            "name": "Afaq Donor",
            "email": "donor@afaq.org",
            "password": "secret123"
        }
    )

    donor_id = user_response.get_json()["user"]["id"]

    project_response = client.post(
        "/api/projects",
        json={
            "title": "Food Support",
            "description": "Supporting families.",
            "category": "Food",
            "location": "Nairobi",
            "target_amount": 50000
        }
    )

    project_id = project_response.get_json()["id"]

    donation_response = client.post(
        "/api/donations",
        json={
            "donor_id": donor_id,
            "project_id": project_id,
            "amount": 5000,
            "payment_method": "M-Pesa"
        }
    )

    assert donation_response.status_code == 201

    project_response = client.get(
        f"/api/projects/{project_id}"
    )

    project = project_response.get_json()

    assert project["amount_raised"] == 5000.0


def test_create_event(client):
    response = client.post(
        "/api/events",
        json={
            "title": "Community Food Drive",
            "description": "Food distribution.",
            "location": "Nairobi",
            "event_date": "2026-10-10",
            "capacity": 50
        }
    )

    assert response.status_code == 201

    event = response.get_json()

    assert event["capacity"] == 50
    assert event["status"] == "upcoming"


def test_volunteer_registration(client):
    user_response = client.post(
        "/api/auth/register",
        json={
            "name": "Volunteer Member",
            "email": "volunteer@afaq.org",
            "password": "secret123"
        }
    )

    member_id = user_response.get_json()["user"]["id"]

    event_response = client.post(
        "/api/events",
        json={
            "title": "Community Event",
            "description": "Helping the community.",
            "location": "Nairobi",
            "event_date": "2026-10-10",
            "capacity": 20
        }
    )

    event_id = event_response.get_json()["id"]

    response = client.post(
        f"/api/events/{event_id}/volunteers",
        json={
            "member_id": member_id
        }
    )

    assert response.status_code == 201

    volunteer = response.get_json()

    assert volunteer["member_id"] == member_id
    assert volunteer["event_id"] == event_id
    