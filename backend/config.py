from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Code Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api"

    # OpenAI
    openai_api_key: str = ""  # Optional - users provide their own
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 4000

    # CORS
    cors_origins: List[str] = []
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]

    # Redis Cache (optional)
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    use_cache: bool = False

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 10080

    # Supported Languages
    programming_languages: List[str] = [
        "python",
        "javascript",
        "typescript",
        "java",
        "csharp",
        "go",
        "rust",
        "cpp",
        "ruby",
        "swift"
    ]

    natural_languages: List[str] = [
        "english",
        "spanish",
        "french",
        "german",
        "chinese",
        "japanese",
        "portuguese",
        "italian",
        "russian",
        "arabic"
    ]

    # Generation Limits
    max_concurrent_generations: int = 3
    max_code_length: int = 10000
    max_prompt_length: int = 2000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()