from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from enum import Enum


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    RUBY = "ruby"
    SWIFT = "swift"


class NaturalLanguage(str, Enum):
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"
    CHINESE = "chinese"
    JAPANESE = "japanese"
    PORTUGUESE = "portuguese"
    ITALIAN = "italian"
    RUSSIAN = "russian"
    ARABIC = "arabic"


class GenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The prompt describing what code to generate"
    )
    programming_language: ProgrammingLanguage = Field(
        ...,
        description="Target programming language for code generation"
    )
    natural_language: NaturalLanguage = Field(
        default=NaturalLanguage.ENGLISH,
        description="Natural language for prompts and documentation"
    )
    project_goals: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional project goals and context"
    )
    include_tests: bool = Field(
        default=True,
        description="Whether to generate unit tests"
    )
    include_docs: bool = Field(
        default=True,
        description="Whether to generate documentation"
    )
    test_framework: Optional[str] = Field(
        default=None,
        description="Specific test framework to use (auto-detected if not specified)"
    )
    style_guide: Optional[str] = Field(
        default=None,
        description="Specific style guide to follow"
    )
    complexity_level: Literal["simple", "intermediate", "advanced"] = Field(
        default="intermediate",
        description="Code complexity level"
    )

    @validator("prompt")
    def validate_prompt(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Prompt must be at least 10 characters long")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Create a function that calculates fibonacci numbers recursively with memoization",
                "programming_language": "python",
                "natural_language": "english",
                "project_goals": "Build efficient mathematical utilities",
                "include_tests": True,
                "include_docs": True,
                "complexity_level": "intermediate"
            }
        }


class AnalysisRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Code to analyze"
    )
    language: ProgrammingLanguage = Field(
        ...,
        description="Programming language of the code"
    )
    check_syntax: bool = Field(
        default=True,
        description="Check syntax validity"
    )
    check_complexity: bool = Field(
        default=True,
        description="Analyze code complexity"
    )
    suggest_improvements: bool = Field(
        default=True,
        description="Provide improvement suggestions"
    )
    format_code: bool = Field(
        default=False,
        description="Format the code according to language standards"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": "def hello():\n    print('Hello, World!')",
                "language": "python",
                "check_syntax": True,
                "check_complexity": True,
                "suggest_improvements": True,
                "format_code": False
            }
        }


class BatchGenerationRequest(BaseModel):
    requests: List[GenerationRequest] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="List of generation requests (max 3)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "requests": [
                    {
                        "prompt": "Create a REST API endpoint for user authentication",
                        "programming_language": "python",
                        "include_tests": True
                    },
                    {
                        "prompt": "Build a React component for a login form",
                        "programming_language": "typescript",
                        "include_tests": True
                    }
                ]
            }
        }