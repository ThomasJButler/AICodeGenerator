from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class GenerationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CodeMetrics(BaseModel):
    lines_of_code: int = Field(description="Total lines of code")
    cyclomatic_complexity: int = Field(description="Cyclomatic complexity score")
    readability_score: float = Field(description="Code readability score (0-100)")
    estimated_execution_time: Optional[str] = Field(
        default=None,
        description="Estimated execution time complexity"
    )
    memory_complexity: Optional[str] = Field(
        default=None,
        description="Estimated memory complexity"
    )


class TestResult(BaseModel):
    test_code: str = Field(description="Generated test code")
    framework: str = Field(description="Test framework used")
    coverage_estimate: float = Field(description="Estimated test coverage percentage")
    test_count: int = Field(description="Number of test cases")


class Documentation(BaseModel):
    inline_comments: str = Field(description="Code with inline comments")
    readme: Optional[str] = Field(default=None, description="README documentation")
    api_docs: Optional[str] = Field(default=None, description="API documentation")
    usage_examples: List[str] = Field(default_factory=list, description="Usage examples")


class GenerationResponse(BaseModel):
    id: str = Field(description="Unique generation ID")
    status: GenerationStatus = Field(description="Generation status")
    code: Optional[str] = Field(default=None, description="Generated code")
    language: str = Field(description="Programming language")
    tests: Optional[TestResult] = Field(default=None, description="Generated tests")
    documentation: Optional[Documentation] = Field(default=None, description="Generated documentation")
    metrics: Optional[CodeMetrics] = Field(default=None, description="Code quality metrics")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "gen_123456",
                "status": "completed",
                "code": "def fibonacci(n, memo={}):\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\n    return memo[n]",
                "language": "python",
                "tests": {
                    "test_code": "import unittest\n\nclass TestFibonacci(unittest.TestCase):\n    def test_base_cases(self):\n        self.assertEqual(fibonacci(0), 0)\n        self.assertEqual(fibonacci(1), 1)",
                    "framework": "unittest",
                    "coverage_estimate": 85.0,
                    "test_count": 5
                },
                "metrics": {
                    "lines_of_code": 7,
                    "cyclomatic_complexity": 3,
                    "readability_score": 92.5,
                    "estimated_execution_time": "O(n)",
                    "memory_complexity": "O(n)"
                },
                "created_at": "2024-01-13T10:00:00Z",
                "processing_time": 2.5
            }
        }


class AnalysisResponse(BaseModel):
    syntax_valid: bool = Field(description="Whether the code is syntactically valid")
    language: str = Field(description="Detected/specified language")
    complexity: int = Field(description="Cyclomatic complexity score")
    readability_score: float = Field(description="Code readability score (0-100)")
    performance_score: float = Field(description="Performance score (0-100)")
    lines_of_code: int = Field(description="Total lines of code")
    syntax_errors: List[Dict[str, Any]] = Field(default_factory=list, description="List of syntax errors")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    metrics: Optional[CodeMetrics] = Field(default=None, description="Additional code quality metrics")
    formatted_code: Optional[str] = Field(default=None, description="Formatted version of the code")
    ast_structure: Optional[Dict[str, Any]] = Field(default=None, description="Abstract syntax tree structure")

    class Config:
        json_schema_extra = {
            "example": {
                "syntax_valid": True,
                "language": "python",
                "complexity": 2,
                "readability_score": 88.5,
                "performance_score": 75.0,
                "lines_of_code": 10,
                "syntax_errors": [],
                "suggestions": [
                    "Consider adding type hints",
                    "Add docstring to function"
                ],
                "metrics": {
                    "lines_of_code": 10,
                    "cyclomatic_complexity": 2,
                    "readability_score": 88.5
                },
                "formatted_code": "def hello():\n    print('Hello, World!')"
            }
        }


class LanguagesResponse(BaseModel):
    programming_languages: List[Dict[str, str]] = Field(
        description="List of supported programming languages"
    )
    natural_languages: List[Dict[str, str]] = Field(
        description="List of supported natural languages"
    )
    test_frameworks: Dict[str, List[str]] = Field(
        description="Test frameworks by language"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "programming_languages": [
                    {"code": "python", "name": "Python", "version": "3.9+"},
                    {"code": "javascript", "name": "JavaScript", "version": "ES6+"}
                ],
                "natural_languages": [
                    {"code": "english", "name": "English"},
                    {"code": "spanish", "name": "Spanish"}
                ],
                "test_frameworks": {
                    "python": ["unittest", "pytest", "nose2"],
                    "javascript": ["jest", "mocha", "jasmine"]
                }
            }
        }


class HealthResponse(BaseModel):
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = Field(description="Status of dependent services")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-13T10:00:00Z",
                "services": {
                    "openai": "connected",
                    "redis": "connected",
                    "tree_sitter": "operational"
                }
            }
        }


class ErrorResponse(BaseModel):
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    status_code: int = Field(description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "The prompt field is required",
                "status_code": 400,
                "timestamp": "2024-01-13T10:00:00Z"
            }
        }