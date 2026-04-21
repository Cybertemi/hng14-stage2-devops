import pytest
import fakeredis
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from main import app


# ─────────────────────────────────────────────
# Setup: swap real Redis for fakeredis
# patches the module-level 'r' variable
# ─────────────────────────────────────────────
@pytest.fixture
def client():
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    with patch('main.r', fake_redis):
        with TestClient(app) as c:
            yield c


# ─────────────────────────────────────────────
# Test 1: Health check returns 200 + ok status
# ─────────────────────────────────────────────
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


# ─────────────────────────────────────────────
# Test 2: Create job returns job_id
# ─────────────────────────────────────────────
def test_create_job_returns_job_id(client):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    # API returns "job_id" not "id"
    assert "job_id" in data
    assert data["job_id"] is not None
    # job_id should be a valid UUID string
    assert len(data["job_id"]) == 36


# ─────────────────────────────────────────────
# Test 3: Created job is pushed onto Redis queue
# ─────────────────────────────────────────────
def test_create_job_pushed_to_redis_queue(client):
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    with patch('main.r', fake_redis):
        with TestClient(app) as c:
            c.post("/jobs")
            # Redis list "job" should have exactly 1 item
            queue_length = fake_redis.llen("job")
            assert queue_length == 1


# ─────────────────────────────────────────────
# Test 4: Get job status returns queued
# after creation
# ─────────────────────────────────────────────
def test_get_job_status_after_creation(client):
    # Create a job first
    create_response = client.post("/jobs")
    assert create_response.status_code == 200
    job_id = create_response.json()["job_id"]

    # Fetch its status
    status_response = client.get(f"/jobs/{job_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["job_id"] == job_id
    assert data["status"] == "queued"


# ─────────────────────────────────────────────
# Test 5: Get status for non-existent job
# returns 404
# ─────────────────────────────────────────────
def test_get_nonexistent_job_returns_404(client):
    response = client.get("/jobs/this-job-does-not-exist")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Job not found"
