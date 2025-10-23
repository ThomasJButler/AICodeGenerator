"""
@author Tom Butler
@date 2025-10-23
@description Language capabilities endpoint.
             Returns supported programming languages, natural languages, and test frameworks.
"""
from fastapi import APIRouter, status
import logging

from models import LanguagesResponse
from config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get(
    "/languages",
    response_model=LanguagesResponse,
    status_code=status.HTTP_200_OK
)
async def get_supported_languages():
    """
    Returns all supported languages and test frameworks.

    Returns:
        LanguagesResponse with programming languages, natural languages, and framework mappings
    """
    try:
        # Programming languages with details
        programming_languages = [
            {"code": "python", "name": "Python", "version": "3.8+"},
            {"code": "javascript", "name": "JavaScript", "version": "ES6+"},
            {"code": "typescript", "name": "TypeScript", "version": "4.0+"},
            {"code": "java", "name": "Java", "version": "11+"},
            {"code": "csharp", "name": "C#", "version": ".NET 6+"},
            {"code": "go", "name": "Go", "version": "1.16+"},
            {"code": "rust", "name": "Rust", "version": "2021 Edition"},
            {"code": "cpp", "name": "C++", "version": "C++17"},
            {"code": "ruby", "name": "Ruby", "version": "3.0+"},
            {"code": "swift", "name": "Swift", "version": "5.0+"}
        ]

        # Natural languages
        natural_languages = [
            {"code": "english", "name": "English"},
            {"code": "spanish", "name": "Spanish"},
            {"code": "french", "name": "French"},
            {"code": "german", "name": "German"},
            {"code": "chinese", "name": "Chinese (Simplified)"},
            {"code": "japanese", "name": "Japanese"},
            {"code": "portuguese", "name": "Portuguese"},
            {"code": "italian", "name": "Italian"},
            {"code": "russian", "name": "Russian"},
            {"code": "arabic", "name": "Arabic"}
        ]

        # Test frameworks by language
        test_frameworks = {
            "python": ["pytest", "unittest", "nose2", "doctest"],
            "javascript": ["jest", "mocha", "jasmine", "vitest", "cypress"],
            "typescript": ["jest", "mocha", "jasmine", "vitest", "cypress"],
            "java": ["junit", "testng", "mockito", "assertj"],
            "csharp": ["xunit", "nunit", "mstest"],
            "go": ["testing", "testify", "ginkgo"],
            "rust": ["cargo test", "proptest"],
            "cpp": ["gtest", "catch2", "boost.test"],
            "ruby": ["rspec", "minitest", "cucumber"],
            "swift": ["xctest", "quick"]
        }

        return LanguagesResponse(
            programming_languages=programming_languages,
            natural_languages=natural_languages,
            test_frameworks=test_frameworks
        )

    except Exception as e:
        logger.error(f"Failed to get languages: {str(e)}")
        raise


@router.get(
    "/languages/programming",
    response_model=list,
    status_code=status.HTTP_200_OK
)
async def get_programming_languages():
    """Get only supported programming languages"""
    return settings.programming_languages


@router.get(
    "/languages/natural",
    response_model=list,
    status_code=status.HTTP_200_OK
)
async def get_natural_languages():
    """Get only supported natural languages"""
    return settings.natural_languages


@router.get(
    "/languages/{language}/frameworks",
    response_model=list,
    status_code=status.HTTP_200_OK
)
async def get_test_frameworks(language: str):
    """Get test frameworks for a specific language"""
    frameworks = {
        "python": ["pytest", "unittest", "nose2", "doctest"],
        "javascript": ["jest", "mocha", "jasmine", "vitest", "cypress"],
        "typescript": ["jest", "mocha", "jasmine", "vitest", "cypress"],
        "java": ["junit", "testng", "mockito", "assertj"],
        "csharp": ["xunit", "nunit", "mstest"],
        "go": ["testing", "testify", "ginkgo"],
        "rust": ["cargo test", "proptest"],
        "cpp": ["gtest", "catch2", "boost.test"],
        "ruby": ["rspec", "minitest", "cucumber"],
        "swift": ["xctest", "quick"]
    }

    return frameworks.get(language, [])