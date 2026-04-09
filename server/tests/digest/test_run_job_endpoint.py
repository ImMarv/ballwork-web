"""Integration tests for the digest run_job endpoint."""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(db_session):
    """FastAPI test client with overridden database dependency."""
    # Import here (after conftest.py sets env vars)
    from app.db import get_db
    from app.main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    # Clean up
    app.dependency_overrides.clear()


class TestDigestRunJobEndpoint:
    """Test the /digest/run_job endpoint."""

    def test_run_job_missing_email_and_id(self, client):
        """Test endpoint returns 400 when neither email nor ID provided."""
        now = datetime.utcnow()
        start = (now - timedelta(hours=24)).isoformat()
        end = (now + timedelta(hours=1)).isoformat()

        response = client.post(
            "/digest/run_job",
            json={
                "start": start,
                "end": end,
            },
        )

        assert response.status_code == 400
        assert "must be provided" in response.json()["detail"]

    def test_run_job_nonexistent_subscriber(self, client):
        """Test endpoint returns 404 for nonexistent subscriber."""
        now = datetime.utcnow()
        start = (now - timedelta(hours=24)).isoformat()
        end = (now + timedelta(hours=1)).isoformat()

        response = client.post(
            "/digest/run_job",
            json={
                "subscriber_email": "nonexistent@example.com",
                "start": start,
                "end": end,
            },
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
