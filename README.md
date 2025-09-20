# AI Code Generator

A powerful AI-powered code generation platform that creates production-ready code with unit tests and documentation.

<img width="1382" height="843" alt="image" src="https://github.com/user-attachments/assets/b91e798e-df62-48c5-8100-6ad043edcabc" />

## Features

- 🚀 **Multi-Language Support**: Generate code in Python, JavaScript, TypeScript, Java, C#, Go, Rust, C++, Ruby, and Swift
- 🧪 **Automatic Test Generation**: Creates comprehensive unit tests with framework detection
- 📚 **Documentation Generation**: Generates inline comments, README files, and API documentation
- 🎯 **Code Quality Metrics**: Analyzes complexity, readability, and performance
- 🌍 **Multi-Language Prompts**: Support for prompts in multiple natural languages
- 🎨 **Matrix-Themed UI**: Stunning cyberpunk-inspired interface with animations

## Architecture

```
Frontend (Next.js + TypeScript + Tailwind)
    ↓
Backend API (FastAPI)
    ├── LangChain (AI Code Generation)
    └── Tree-sitter (Code Analysis)
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn openai python-dotenv
```

4. Create `.env` file:
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

5. Run the backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000)

## Usage

1. Enter a description of what you want to build
2. Select your target programming language
3. Optionally specify project goals
4. Choose whether to generate tests and documentation
5. Click "GENERATE CODE"
6. View generated code, tests, and documentation in tabs
7. Copy or download the results

## API Endpoints

- `POST /api/generate` - Generate code from a prompt
- `POST /api/analyze` - Analyze code quality
- `GET /api/languages` - Get supported languages
- `GET /api/health` - Health check

## Environment Variables

### Backend
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000/api)

## Tech Stack

### Backend
- FastAPI - Web framework
- LangChain - AI orchestration
- OpenAI API - Code generation
- Tree-sitter - Code parsing
- Pydantic - Data validation

### Frontend
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Framer Motion - Animations
- React Syntax Highlighter - Code display

## Features in Detail

### Code Generation
- Syntactically correct code following best practices
- Error handling and optimization included
- Supports multiple complexity levels
- Context-aware generation based on project goals

### Test Generation
- Framework-specific tests (pytest, jest, junit, etc.)
- Edge case coverage
- Mock implementations where needed
- Coverage estimation

### Documentation
- Inline code comments
- Function/class documentation
- README generation
- API documentation
- Usage examples

### Code Analysis
- Syntax validation
- Cyclomatic complexity calculation
- Readability scoring
- Performance estimation
- Improvement suggestions

## Matrix Theme

The UI features a cyberpunk Matrix-inspired theme with:
- Green-on-black terminal aesthetic
- Glitch effects and animations
- Typing animations
- Scan line effects
- Custom scrollbars
- Loading animations

## Development

### Project Structure
```
AICodeGenerator/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API endpoints
│   ├── services/            # Business logic
│   └── models/              # Data models
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   └── public/              # Static assets
└── CLAUDE.md                # Development guide
```

## License

MIT

## Credits

Built with ❤️ using AI-powered development tools
