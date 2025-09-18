"""Integration tests for languages endpoint."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestLanguagesEndpoint:
    """Test suite for languages endpoint."""

    def test_get_languages_returns_200(self, test_client: TestClient):
        """Test that languages endpoint returns 200 status."""
        response = test_client.get("/api/languages")
        assert response.status_code == 200

    def test_get_languages_response_structure(self, test_client: TestClient):
        """Test languages response has correct structure."""
        response = test_client.get("/api/languages")
        data = response.json()

        assert "languages" in data
        assert isinstance(data["languages"], list)
        assert len(data["languages"]) > 0

    def test_get_languages_contains_expected_languages(self, test_client: TestClient):
        """Test that response contains all expected programming languages."""
        expected_languages = [
            "python", "javascript", "typescript", "java",
            "csharp", "go", "rust", "cpp", "ruby", "swift"
        ]

        response = test_client.get("/api/languages")
        data = response.json()

        languages = data["languages"]
        language_values = [lang["value"] for lang in languages]

        for expected in expected_languages:
            assert expected in language_values, f"Missing language: {expected}"

    def test_language_object_structure(self, test_client: TestClient):
        """Test that each language object has correct structure."""
        response = test_client.get("/api/languages")
        data = response.json()

        for language in data["languages"]:
            assert "value" in language
            assert "label" in language
            assert "extension" in language
            assert "test_framework" in language
            assert isinstance(language["value"], str)
            assert isinstance(language["label"], str)
            assert isinstance(language["extension"], str)

    def test_language_metadata_correctness(self, test_client: TestClient):
        """Test that language metadata is correct."""
        response = test_client.get("/api/languages")
        data = response.json()

        # Check a few specific languages for correct metadata
        languages_dict = {lang["value"]: lang for lang in data["languages"]}

        # Python
        assert languages_dict["python"]["extension"] == ".py"
        assert languages_dict["python"]["label"] == "Python"
        assert "pytest" in languages_dict["python"]["test_framework"].lower()

        # JavaScript
        assert languages_dict["javascript"]["extension"] == ".js"
        assert languages_dict["javascript"]["label"] == "JavaScript"
        assert "jest" in languages_dict["javascript"]["test_framework"].lower()

        # TypeScript
        assert languages_dict["typescript"]["extension"] == ".ts"
        assert languages_dict["typescript"]["label"] == "TypeScript"

        # Java
        assert languages_dict["java"]["extension"] == ".java"
        assert languages_dict["java"]["label"] == "Java"
        assert "junit" in languages_dict["java"]["test_framework"].lower()

    def test_languages_endpoint_is_cached(self, test_client: TestClient):
        """Test that languages endpoint returns consistent results (cached)."""
        response1 = test_client.get("/api/languages")
        response2 = test_client.get("/api/languages")

        assert response1.json() == response2.json()

    def test_languages_sorted_alphabetically(self, test_client: TestClient):
        """Test that languages are sorted alphabetically by label."""
        response = test_client.get("/api/languages")
        data = response.json()

        labels = [lang["label"] for lang in data["languages"]]
        assert labels == sorted(labels), "Languages should be sorted alphabetically"