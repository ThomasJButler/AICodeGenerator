"""Integration tests for code analysis endpoint."""
import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestAnalyzeEndpoint:
    """Test suite for code analysis endpoint."""

    def test_analyze_valid_python_code(
        self,
        test_client: TestClient,
        sample_analyze_request
    ):
        """Test analyzing valid Python code."""
        response = test_client.post("/api/analyze", json=sample_analyze_request)

        assert response.status_code == 200
        data = response.json()

        assert "syntax_valid" in data
        assert "complexity" in data
        assert "readability_score" in data
        assert "performance_score" in data
        assert "suggestions" in data

    def test_analyze_invalid_syntax(self, test_client: TestClient):
        """Test analyzing code with syntax errors."""
        request = {
            "code": "def broken_function(\n    print('missing closing parenthesis'",
            "language": "python"
        }

        response = test_client.post("/api/analyze", json=request)

        assert response.status_code == 200
        data = response.json()

        assert data["syntax_valid"] is False
        assert "syntax_errors" in data
        assert len(data["syntax_errors"]) > 0

    def test_analyze_complex_code(self, test_client: TestClient):
        """Test analyzing complex code with high cyclomatic complexity."""
        complex_code = """
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            if z > 0:
                return x + z
            else:
                return x
    else:
        if y > 0:
            if z > 0:
                return y + z
            else:
                return y
        else:
            if z > 0:
                return z
            else:
                return 0
"""

        request = {
            "code": complex_code,
            "language": "python"
        }

        response = test_client.post("/api/analyze", json=request)

        assert response.status_code == 200
        data = response.json()

        assert data["syntax_valid"] is True
        assert data["complexity"] > 5  # High complexity
        assert len(data["suggestions"]) > 0

    def test_analyze_empty_code(self, test_client: TestClient):
        """Test analyzing empty code."""
        request = {
            "code": "",
            "language": "python"
        }

        response = test_client.post("/api/analyze", json=request)

        assert response.status_code == 200
        data = response.json()

        assert data["syntax_valid"] is True
        assert data["complexity"] == 1
        assert data["lines_of_code"] == 0

    def test_analyze_javascript_code(self, test_client: TestClient):
        """Test analyzing JavaScript code."""
        request = {
            "code": """
function helloWorld() {
    console.log("Hello, World!");
    return true;
}
""",
            "language": "javascript"
        }

        response = test_client.post("/api/analyze", json=request)

        assert response.status_code == 200
        data = response.json()

        assert data["syntax_valid"] is True
        assert "complexity" in data
        assert "lines_of_code" in data

    def test_analyze_missing_code(self, test_client: TestClient):
        """Test analysis with missing code field."""
        request = {
            "language": "python"
        }

        response = test_client.post("/api/analyze", json=request)
        assert response.status_code == 422

    def test_analyze_missing_language(self, test_client: TestClient):
        """Test analysis with missing language field."""
        request = {
            "code": "print('hello')"
        }

        response = test_client.post("/api/analyze", json=request)
        assert response.status_code == 422

    def test_analyze_with_performance_metrics(self, test_client: TestClient):
        """Test that analysis includes performance metrics."""
        request = {
            "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
            "language": "python"
        }

        response = test_client.post("/api/analyze", json=request)

        assert response.status_code == 200
        data = response.json()

        assert "performance_score" in data
        assert data["performance_score"] >= 0
        assert data["performance_score"] <= 100

        # Should have suggestions about recursion
        assert any("recursion" in s.lower() or "performance" in s.lower()
                  for s in data.get("suggestions", []))