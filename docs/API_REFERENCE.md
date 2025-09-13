# API Reference

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication. In production, implement API key or JWT authentication.

## Endpoints

### 1. Generate Code

Generate code from a natural language prompt.

**Endpoint**: `POST /api/generate`

**Request Body**:
```json
{
  "prompt": "Create a function that calculates fibonacci numbers",
  "programming_language": "python",
  "natural_language": "english",
  "project_goals": "Build efficient mathematical utilities",
  "include_tests": true,
  "include_docs": true,
  "test_framework": "pytest",
  "style_guide": "PEP 8",
  "complexity_level": "intermediate"
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Description of code to generate (1-2000 chars) |
| programming_language | enum | Yes | Target programming language |
| natural_language | enum | No | Language for prompts/docs (default: english) |
| project_goals | string | No | Optional context (max 500 chars) |
| include_tests | boolean | No | Generate unit tests (default: true) |
| include_docs | boolean | No | Generate documentation (default: true) |
| test_framework | string | No | Specific test framework |
| style_guide | string | No | Code style to follow |
| complexity_level | enum | No | simple, intermediate, advanced |

**Response** (200 OK):
```json
{
  "id": "gen_abc123",
  "status": "completed",
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "tests": {
    "test_code": "import pytest\n\ndef test_fibonacci():\n    assert fibonacci(0) == 0\n    assert fibonacci(1) == 1",
    "framework": "pytest",
    "coverage_estimate": 85.0,
    "test_count": 5
  },
  "documentation": {
    "inline_comments": "# Code with comments...",
    "readme": "## Fibonacci Function\n\nCalculates fibonacci numbers...",
    "api_docs": null,
    "usage_examples": [
      "result = fibonacci(10)",
      "print(fibonacci(5))"
    ]
  },
  "metrics": {
    "lines_of_code": 4,
    "cyclomatic_complexity": 2,
    "readability_score": 92.5,
    "estimated_execution_time": "O(2^n)",
    "memory_complexity": "O(n)"
  },
  "created_at": "2024-01-13T10:00:00Z",
  "processing_time": 2.5
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Invalid request",
  "detail": "Prompt must be at least 10 characters long",
  "status_code": 400,
  "timestamp": "2024-01-13T10:00:00Z"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Code generation failed",
  "detail": "AI service temporarily unavailable",
  "status_code": 500,
  "timestamp": "2024-01-13T10:00:00Z"
}
```

---

### 2. Batch Generate

Generate multiple code snippets concurrently (max 3).

**Endpoint**: `POST /api/generate/batch`

**Request Body**:
```json
{
  "requests": [
    {
      "prompt": "Create a REST API endpoint",
      "programming_language": "python",
      "include_tests": true
    },
    {
      "prompt": "Build a React component",
      "programming_language": "typescript",
      "include_tests": true
    }
  ]
}
```

**Response** (200 OK):
```json
[
  {
    "id": "gen_abc123",
    "status": "completed",
    "code": "...",
    "language": "python"
  },
  {
    "id": "gen_def456",
    "status": "completed",
    "code": "...",
    "language": "typescript"
  }
]
```

---

### 3. Analyze Code

Analyze code for syntax, complexity, and quality.

**Endpoint**: `POST /api/analyze`

**Request Body**:
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "language": "python",
  "check_syntax": true,
  "check_complexity": true,
  "suggest_improvements": true,
  "format_code": false
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | string | Yes | Code to analyze (1-10000 chars) |
| language | enum | Yes | Programming language |
| check_syntax | boolean | No | Validate syntax (default: true) |
| check_complexity | boolean | No | Calculate complexity (default: true) |
| suggest_improvements | boolean | No | Provide suggestions (default: true) |
| format_code | boolean | No | Format the code (default: false) |

**Response** (200 OK):
```json
{
  "valid": true,
  "language": "python",
  "metrics": {
    "lines_of_code": 2,
    "cyclomatic_complexity": 1,
    "readability_score": 95.0,
    "estimated_execution_time": "O(1)",
    "memory_complexity": "O(1)"
  },
  "issues": [],
  "suggestions": [
    "Consider adding a docstring",
    "Add type hints for better clarity"
  ],
  "formatted_code": null,
  "ast_structure": {
    "type": "Module",
    "children": [...]
  }
}
```

---

### 4. Format Code

Format code according to language standards.

**Endpoint**: `POST /api/analyze/format`

**Request Body**:
```json
{
  "code": "def hello():print('Hello')",
  "language": "python"
}
```

**Response** (200 OK):
```json
{
  "formatted_code": "def hello():\n    print('Hello')",
  "language": "python"
}
```

---

### 5. Validate Syntax

Check if code syntax is valid.

**Endpoint**: `POST /api/analyze/validate`

**Request Body**:
```json
{
  "code": "def hello()\n    print('Hello')",
  "language": "python"
}
```

**Response** (200 OK):
```json
{
  "valid": false,
  "language": "python",
  "issues": [
    {
      "type": "error",
      "line": 1,
      "column": 11,
      "message": "Syntax error: expected ':'"
    }
  ]
}
```

---

### 6. Get Supported Languages

Get all supported programming and natural languages.

**Endpoint**: `GET /api/languages`

**Response** (200 OK):
```json
{
  "programming_languages": [
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
  ],
  "natural_languages": [
    {"code": "english", "name": "English"},
    {"code": "spanish", "name": "Spanish"},
    {"code": "french", "name": "French"},
    {"code": "german", "name": "German"},
    {"code": "chinese", "name": "Chinese (Simplified)"}
  ],
  "test_frameworks": {
    "python": ["pytest", "unittest", "nose2", "doctest"],
    "javascript": ["jest", "mocha", "jasmine", "vitest"],
    "typescript": ["jest", "mocha", "jasmine", "vitest"],
    "java": ["junit", "testng", "mockito"],
    "csharp": ["xunit", "nunit", "mstest"]
  }
}
```

---

### 7. Get Programming Languages

Get only supported programming languages.

**Endpoint**: `GET /api/languages/programming`

**Response** (200 OK):
```json
[
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
```

---

### 8. Get Test Frameworks

Get test frameworks for a specific language.

**Endpoint**: `GET /api/languages/{language}/frameworks`

**Parameters**:
- `language` (path): Programming language code

**Example**: `GET /api/languages/python/frameworks`

**Response** (200 OK):
```json
[
  "pytest",
  "unittest",
  "nose2",
  "doctest"
]
```

---

### 9. Health Check

Check API and service health status.

**Endpoint**: `GET /api/health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-13T10:00:00Z",
  "services": {
    "openai": "connected",
    "redis": "disabled",
    "tree_sitter": "operational"
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - AI service down |

## Rate Limiting

Default limits (configurable):
- 100 requests per hour per IP
- 3 concurrent generation requests

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704196800
```

## Data Types

### Programming Language Enum
```
python | javascript | typescript | java | csharp | go | rust | cpp | ruby | swift
```

### Natural Language Enum
```
english | spanish | french | german | chinese | japanese | portuguese | italian | russian | arabic
```

### Complexity Level Enum
```
simple | intermediate | advanced
```

### Generation Status Enum
```
pending | in_progress | completed | failed
```

## Examples

### cURL Example

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to reverse a string",
    "programming_language": "python",
    "include_tests": true
  }'
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prompt: 'Create a function to reverse a string',
    programming_language: 'python',
    include_tests: true
  })
});

const data = await response.json();
console.log(data.code);
```

### Python Example

```python
import requests

response = requests.post(
    'http://localhost:8000/api/generate',
    json={
        'prompt': 'Create a function to reverse a string',
        'programming_language': 'python',
        'include_tests': True
    }
)

data = response.json()
print(data['code'])
```

## WebSocket Support (Future)

Planned WebSocket endpoint for real-time generation:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');

ws.send(JSON.stringify({
  prompt: 'Create a REST API',
  programming_language: 'python'
}));

ws.onmessage = (event) => {
  const chunk = JSON.parse(event.data);
  console.log(chunk.content); // Streaming response
};
```

## SDK Support (Future)

Planned SDK packages:
- `@aicodegen/client` - JavaScript/TypeScript
- `aicodegen` - Python
- `aicodegen-java` - Java

## Changelog

### v1.0.0 (Current)
- Initial API release
- Support for 10 programming languages
- Code generation with tests and documentation
- Code analysis and formatting

### Planned v1.1.0
- WebSocket support for streaming
- User authentication
- Generation history
- Custom model support