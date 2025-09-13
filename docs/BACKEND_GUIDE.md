# Backend Development Guide

## Overview

The backend is built with FastAPI, providing a robust REST API for AI-powered code generation. This guide covers the architecture, implementation details, and best practices.

## Architecture

### Layer Structure

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)          │
│         Handles HTTP concerns        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│        Service Layer                 │
│     Business Logic & AI Calls        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│         External Services            │
│    OpenAI API, Tree-sitter           │
└─────────────────────────────────────┘
```

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── api/
│   └── endpoints/
│       ├── generate.py    # Code generation endpoints
│       ├── analyze.py     # Code analysis endpoints
│       ├── languages.py   # Language support endpoints
│       └── health.py      # Health check
├── services/
│   ├── code_generator.py  # LangChain integration
│   └── code_analyzer.py   # Tree-sitter integration
└── models/
    ├── request.py         # Request DTOs
    └── response.py        # Response DTOs
```

## Core Components

### 1. FastAPI Application (main.py)

**Purpose**: Application bootstrap and middleware configuration

```python
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url=f"{settings.api_prefix}/docs"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True
)
```

**Key Features**:
- Automatic API documentation at `/api/docs`
- CORS support for frontend integration
- Structured logging
- Graceful startup/shutdown

### 2. Configuration Management (config.py)

**Pattern**: Pydantic Settings for type-safe configuration

```python
class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"

    class Config:
        env_file = ".env"
```

**Benefits**:
- Environment variables automatically loaded
- Type validation at startup
- Single source of truth for configuration

### 3. Service Layer

#### Code Generator Service

**Responsibility**: AI-powered code generation

```python
class CodeGeneratorService:
    async def generate_code(self, request: GenerationRequest) -> str:
        prompt = self._create_code_prompt(request)
        response = await self.llm.ainvoke(prompt)
        return self._extract_code(response)
```

**Key Methods**:
- `generate_code()`: Main generation logic
- `generate_tests()`: Unit test creation
- `generate_documentation()`: Doc generation
- `calculate_metrics()`: Quality metrics

**Prompt Engineering Strategy**:

```python
def _create_code_prompt(self, request):
    return f"""
    You are an expert programmer.

    Requirements:
    1. Code must be syntactically correct
    2. Follow {language} best practices
    3. Include error handling

    Prompt: {request.prompt}
    """
```

#### Code Analyzer Service

**Responsibility**: Code validation and analysis

```python
class CodeAnalyzerService:
    def analyze_code(self, request: AnalysisRequest):
        # Parse with Tree-sitter
        tree = self.parser.parse(code)

        # Find syntax errors
        errors = self._find_syntax_errors(tree)

        # Calculate metrics
        metrics = self._calculate_metrics(code)

        return AnalysisResult(...)
```

**Analysis Features**:
- Syntax validation
- Cyclomatic complexity calculation
- Readability scoring
- Performance estimation

### 4. API Endpoints

#### Generation Endpoint

```python
@router.post("/generate")
async def generate_code(request: GenerationRequest):
    # Input validation handled by Pydantic
    code = await generator_service.generate_code(request)

    # Optional test generation
    if request.include_tests:
        tests = await generator_service.generate_tests(code)

    return GenerationResponse(...)
```

**Features**:
- Async request handling
- Automatic validation
- Conditional processing
- Structured responses

#### Batch Generation

```python
@router.post("/generate/batch")
async def generate_batch(batch: BatchGenerationRequest):
    # Process concurrently
    tasks = [generate_code_async(req) for req in batch.requests]
    results = await asyncio.gather(*tasks)
    return results
```

**Concurrency Strategy**:
- Parallel processing of multiple requests
- Graceful error handling per request
- Maximum 3 concurrent generations

## Data Models

### Request Models

```python
class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    programming_language: ProgrammingLanguage
    include_tests: bool = True
    include_docs: bool = True

    @validator("prompt")
    def validate_prompt(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Prompt too short")
        return v.strip()
```

**Validation Features**:
- Field-level constraints
- Custom validators
- Enum validation for languages
- Automatic documentation

### Response Models

```python
class GenerationResponse(BaseModel):
    id: str
    status: GenerationStatus
    code: Optional[str]
    tests: Optional[TestResult]
    documentation: Optional[Documentation]
    metrics: Optional[CodeMetrics]
```

**Design Principles**:
- Optional fields for partial success
- Nested models for complex data
- Clear status indication
- Comprehensive error information

## Error Handling

### Structured Exceptions

```python
try:
    result = await generate_code(request)
except OpenAIError as e:
    raise HTTPException(
        status_code=503,
        detail=f"AI service unavailable: {str(e)}"
    )
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )
```

### Error Response Format

```json
{
  "error": "Invalid request",
  "detail": "Programming language 'cobol' not supported",
  "status_code": 400,
  "timestamp": "2024-01-13T10:00:00Z"
}
```

## Performance Optimizations

### 1. Async Operations

All I/O operations use async/await:
```python
async def generate_code():
    # Non-blocking AI calls
    response = await openai_client.chat.completions.create(...)
```

### 2. Connection Pooling

HTTP client reuse:
```python
# Singleton client
http_client = httpx.AsyncClient()

# Reuse across requests
response = await http_client.post(...)
```

### 3. Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_test_framework(language: str):
    # Cache frequently accessed data
    return frameworks[language]
```

## Testing

### Unit Tests

```python
# test_generator.py
async def test_generate_code():
    request = GenerationRequest(
        prompt="Create hello world",
        programming_language="python"
    )

    result = await generator.generate_code(request)

    assert "print" in result
    assert "Hello" in result
```

### Integration Tests

```python
# test_api.py
async def test_generation_endpoint():
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "/api/generate",
            json={"prompt": "test", "programming_language": "python"}
        )

    assert response.status_code == 200
    assert "code" in response.json()
```

## Deployment Considerations

### Environment Variables

Required:
```bash
OPENAI_API_KEY=sk-...
```

Optional:
```bash
REDIS_URL=redis://localhost:6379
RATE_LIMIT_REQUESTS=100
```

### Production Settings

```python
# Production config
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
LOG_LEVEL=INFO
```

### Scaling Strategies

1. **Horizontal Scaling**: Multiple FastAPI workers
2. **Caching**: Redis for frequent requests
3. **Rate Limiting**: Prevent abuse
4. **Queue System**: For long-running generations

## Security Best Practices

### 1. API Key Management

Never commit keys:
```python
# Use environment variables
api_key = os.getenv("OPENAI_API_KEY")
```

### 2. Input Validation

Strict validation:
```python
prompt: str = Field(..., max_length=2000)
```

### 3. Rate Limiting

Prevent abuse:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
async def generate_code():
    pass
```

## Monitoring

### Health Checks

```python
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "openai": check_openai_connection(),
            "database": check_db_connection()
        }
    }
```

### Logging

Structured logging:
```python
logger.info(
    "Code generation completed",
    extra={
        "generation_id": gen_id,
        "language": language,
        "processing_time": time.time() - start
    }
)
```

## Common Issues and Solutions

### Issue 1: Slow Response Times

**Solution**: Implement streaming responses
```python
async def generate_stream():
    async for chunk in openai_stream:
        yield chunk
```

### Issue 2: Memory Leaks

**Solution**: Proper cleanup
```python
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Cleanup
    await http_client.aclose()
```

### Issue 3: Rate Limit Errors

**Solution**: Exponential backoff
```python
@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_openai():
    return await openai_client.chat.completions.create(...)
```

## Development Workflow

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --port 8000

# Run tests
pytest

# Format code
black .
```

### API Documentation

Access at `http://localhost:8000/api/docs`

Features:
- Interactive API testing
- Request/response schemas
- Authentication testing

## Next Steps

1. **Add Authentication**: JWT tokens for user management
2. **Implement Caching**: Redis for response caching
3. **Add Metrics**: Prometheus for monitoring
4. **Create Admin Panel**: Manage configurations
5. **Add WebSockets**: Real-time generation updates