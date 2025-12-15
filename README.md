
A Full-stack code generation platform. Describe what you want, get production-ready code with tests and docs.

<img width="1382" height="843" alt="image" src="https://github.com/user-attachments/assets/b91e798e-df62-48c5-8100-6ad043edcabc" />

## What It Does

Generates code in 10 languages (Python, JavaScript, TypeScript, Java, C#, Go, Rust, C++, Ruby, Swift) using OpenAI's GPT-4. Includes automatic test generation with framework detection and inline documentation. Users provide their own API key stored locally in browser.

## Installation

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Usage

1. Add your OpenAI API key (stored locally in browser)
2. Enter what you want to build
3. Select programming language
4. Generate code, tests, and documentation
5. Copy or download results

## Architecture

```
Frontend (Next.js + TypeScript)
    ↓ HTTP + Auth Header
Backend (FastAPI)
    ↓ User's API Key
OpenAI GPT-4
```

User's OpenAI API key stored in `localStorage`, sent in Authorization header. Backend creates separate LangChain instance per request with provided key.

## API Endpoints

- `POST /api/generate` - Generate code (requires `Authorization: Bearer <api_key>`)
- `POST /api/analyze` - Analyse code quality
- `GET /api/languages` - Supported languages
- `GET /api/health` - Health check

## Environment Variables

**Backend** (`.env`):
```bash
# Optional - users provide their own
OPENAI_API_KEY=""
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Tech Stack

**Backend**: FastAPI, LangChain, OpenAI API, tree-sitter, Pydantic
**Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS, Framer Motion

## Key Features

- Multi-language support with framework-specific test generation
- Code quality metrics (complexity, readability, performance)
- Syntax validation using tree-sitter AST parsing
- Matrix-themed cyberpunk UI
- No API key storage on backend - users bring their own

## Development

Tests: `cd backend && pytest`
Linting: `cd frontend && npm run lint`

See [CLAUDE.md](CLAUDE.md) for detailed development guide.

## License

MIT
