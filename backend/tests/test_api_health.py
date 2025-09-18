"""Integration tests for health check endpoint."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    def test_health_check_returns_200(self, test_client: TestClient):
        """Test that health check endpoint returns 200 status."""
        response = test_client.get("/api/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, test_client: TestClient):
        """Test health check response has correct structure."""
        response = test_client.get("/api/health")
        data = response.json()

        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "services" in data

    def test_health_check_status_value(self, test_client: TestClient):
        """Test health check returns healthy status."""
        response = test_client.get("/api/health")
        data = response.json()

        assert data["status"] == "healthy"
        assert "services" in data
        assert isinstance(data["services"], dict)

    def test_root_endpoint(self, test_client: TestClient):
        """Test root endpoint returns API information."""
        response = test_client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert "api_docs" in data
        assert data["status"] == "operational"