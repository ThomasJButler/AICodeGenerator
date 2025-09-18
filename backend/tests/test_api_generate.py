"""Integration tests for code generation endpoint."""
import pytest
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestGenerateEndpoint:
    """Test suite for code generation endpoint."""

    @patch('services.code_generator.ChatOpenAI')
    def test_generate_code_success(
        self,
        mock_openai,
        test_client: TestClient,
        sample_generation_request,
        mock_openai_response
    ):
        """Test successful code generation."""
        # Setup mock
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_llm.invoke = Mock(return_value=Mock(content=mock_openai_response["choices"][0]["message"]["content"]))

        response = test_client.post("/api/generate", json=sample_generation_request)

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "code" in data
        assert "language" in data
        assert data["language"] == "python"

    def test_generate_code_missing_prompt(self, test_client: TestClient):
        """Test code generation with missing prompt."""
        request_data = {
            "programming_language": "python"
        }

        response = test_client.post("/api/generate", json=request_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_generate_code_invalid_language(self, test_client: TestClient):
        """Test code generation with invalid programming language."""
        request_data = {
            "prompt": "Create a function",
            "programming_language": "invalid_language"
        }

        response = test_client.post("/api/generate", json=request_data)
        assert response.status_code == 422

    @patch('services.code_generator.ChatOpenAI')
    def test_generate_with_tests(
        self,
        mock_openai,
        test_client: TestClient,
        sample_generation_request,
        mock_openai_response,
        mock_openai_test_response
    ):
        """Test code generation with test generation enabled."""
        # Setup mock
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_llm.invoke = Mock(side_effect=[
            Mock(content=mock_openai_response["choices"][0]["message"]["content"]),
            Mock(content=mock_openai_test_response["choices"][0]["message"]["content"])
        ])

        request = sample_generation_request.copy()
        request["include_tests"] = True

        response = test_client.post("/api/generate", json=request)

        assert response.status_code == 200
        data = response.json()

        assert "tests" in data
        assert data["tests"] is not None

    @patch('services.code_generator.ChatOpenAI')
    def test_generate_with_documentation(
        self,
        mock_openai,
        test_client: TestClient,
        sample_generation_request,
        mock_openai_response,
        mock_openai_docs_response
    ):
        """Test code generation with documentation enabled."""
        # Setup mock
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_llm.invoke = Mock(side_effect=[
            Mock(content=mock_openai_response["choices"][0]["message"]["content"]),
            Mock(content=mock_openai_docs_response["choices"][0]["message"]["content"])
        ])

        request = sample_generation_request.copy()
        request["include_documentation"] = True

        response = test_client.post("/api/generate", json=request)

        assert response.status_code == 200
        data = response.json()

        assert "documentation" in data
        assert data["documentation"] is not None

    def test_generate_all_languages(self, test_client: TestClient):
        """Test that all supported languages are accepted."""
        languages = [
            "python", "javascript", "typescript", "java",
            "csharp", "go", "rust", "cpp", "ruby", "swift"
        ]

        for lang in languages:
            with patch('services.code_generator.ChatOpenAI') as mock_openai:
                mock_llm = Mock()
                mock_openai.return_value = mock_llm
                mock_llm.invoke = Mock(return_value=Mock(content="// Sample code"))

                request = {
                    "prompt": "Hello world",
                    "programming_language": lang
                }

                response = test_client.post("/api/generate", json=request)
                assert response.status_code == 200, f"Failed for language: {lang}"

    @patch('services.code_generator.ChatOpenAI')
    def test_generate_with_metrics(
        self,
        mock_openai,
        test_client: TestClient,
        sample_generation_request
    ):
        """Test that code generation includes metrics."""
        # Setup mock
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_llm.invoke = Mock(return_value=Mock(content="def test():\n    pass"))

        response = test_client.post("/api/generate", json=sample_generation_request)

        assert response.status_code == 200
        data = response.json()

        assert "metrics" in data
        if data["metrics"]:
            assert "lines_of_code" in data["metrics"]
            assert "cyclomatic_complexity" in data["metrics"]
            assert "readability_score" in data["metrics"]