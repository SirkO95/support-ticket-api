import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


@pytest.fixture()
def client():
    # Use a separate in-memory SQLite database for every test.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def create_ticket(client, title="Cannot log in", description="Login page returns an error",
                  priority="high"):
    response = client.post(
        "/tickets/",
        json={
            "title": title,
            "description": description,
            "priority": priority,
        },
    )
    return response


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Support Ticket API is running"


def test_create_ticket(client):
    response = create_ticket(client)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Cannot log in"
    assert data["status"] == "open"
    assert data["priority"] == "high"
    assert data["comments"] == []
    assert "id" in data


def test_create_ticket_rejects_short_title(client):
    response = create_ticket(client, title="Oops")
    assert response.status_code == 422


def test_list_tickets(client):
    create_ticket(client, title="First ticket")
    create_ticket(client, title="Second ticket", priority="low")

    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_tickets_by_status_and_priority(client):
    first = create_ticket(client, title="High priority ticket", priority="high").json()
    second = create_ticket(client, title="Low priority ticket", priority="low").json()

    # Update the first ticket so filters can be checked independently.
    client.patch(f"/tickets/{first['id']}", json={"status": "in_progress"})

    by_status = client.get("/tickets/", params={"status": "in_progress"})
    assert [ticket["id"] for ticket in by_status.json()] == [first["id"]]

    by_priority = client.get("/tickets/", params={"priority": "low"})
    assert [ticket["id"] for ticket in by_priority.json()] == [second["id"]]


def test_get_ticket_by_id_and_missing_ticket(client):
    created = create_ticket(client).json()

    response = client.get(f"/tickets/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

    missing = client.get("/tickets/9999")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Ticket not found"


def test_update_ticket(client):
    created = create_ticket(client).json()

    response = client.patch(
        f"/tickets/{created['id']}",
        json={"status": "resolved", "priority": "low"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
    assert response.json()["priority"] == "low"


def test_update_missing_ticket_returns_404(client):
    response = client.patch("/tickets/9999", json={"status": "closed"})
    assert response.status_code == 404


def test_add_comment_to_ticket(client):
    created = create_ticket(client).json()

    response = client.post(
        f"/tickets/{created['id']}/comments",
        json={"author": "Support Agent", "content": "We are investigating."},
    )
    assert response.status_code == 201
    assert response.json()["author"] == "Support Agent"
    assert response.json()["content"] == "We are investigating."

    ticket = client.get(f"/tickets/{created['id']}")
    assert len(ticket.json()["comments"]) == 1


def test_add_comment_to_missing_ticket_returns_404(client):
    response = client.post(
        "/tickets/9999/comments",
        json={"author": "Support Agent", "content": "Hello"},
    )
    assert response.status_code == 404
