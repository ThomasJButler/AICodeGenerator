import os
import sys
import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Generator
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set required environment variables before importing the app
os.environ["OPENAI_API_KEY"] = "test-api-key"
os.environ["DEBUG"] = "True"
os.environ["ENVIRONMENT"] = "testing"

from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_client() -> Generator:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for consistent testing."""
    return {
        "choices": [{
            "message": {
                "content": """def hello_world():
    '''A simple hello world function'''
    return "Hello, World!"
"""
            }
        }]
    }


@pytest.fixture
def mock_openai_test_response():
    """Mock OpenAI API response for test generation."""
    return {
        "choices": [{
            "message": {
                "content": """import unittest

class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        result = hello_world()
        self.assertEqual(result, "Hello, World!")
"""
            }
        }]
    }


@pytest.fixture
def mock_openai_docs_response():
    """Mock OpenAI API response for documentation generation."""
    return {
        "choices": [{
            "message": {
                "content": """# Hello World Function

## Description
A simple function that returns a greeting message.

## Usage
```python
result = hello_world()
print(result)  # Output: Hello, World!
```

## Returns
- str: A greeting message
"""
            }
        }]
    }


@pytest.fixture
def sample_generation_request():
    """Sample request payload for code generation."""
    return {
        "prompt": "Create a hello world function",
        "programming_language": "python",
        "complexity_level": "beginner",
        "include_tests": True,
        "include_documentation": True,
        "project_goals": "Learning basics",
        "style_guide": "PEP8",
        "natural_language": "english"
    }


@pytest.fixture
def sample_analyze_request():
    """Sample request payload for code analysis."""
    return {
        "code": """def hello_world():
    return "Hello, World!"
""",
        "language": "python"
    }


@pytest.fixture
def mock_langchain_chain():
    """Mock LangChain chain for testing."""
    mock_chain = AsyncMock()
    mock_chain.ainvoke.return_value = {
        "text": """def hello_world():
    '''A simple hello world function'''
    return "Hello, World!"
"""
    }
    return mock_chain


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set required environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("API_HOST", "0.0.0.0")
    monkeypatch.setenv("API_PORT", "8000")