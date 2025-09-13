# Frontend Development Guide

## Overview

The frontend is a Next.js application with a Matrix-themed UI that provides an interactive dashboard for AI-powered code generation. This guide covers the implementation details, design decisions, and component architecture.

## Technology Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Animations
- **React Syntax Highlighter**: Code display
- **Axios**: API communication

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx           # Main dashboard page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/
│   ├── CodeDisplay.tsx    # Code viewer component
│   └── MatrixLoader.tsx   # Loading animations
├── public/                # Static assets
└── lib/
    └── api.ts            # API client (future)
```

## Core Components

### 1. Main Dashboard (app/page.tsx)

**Architecture**: Single-page application with local state management

```typescript
export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [results, setResults] = useState<GenerationResult[]>([]);

  const handleGenerate = async () => {
    const response = await axios.post(`${API_URL}/generate`, {
      prompt,
      programming_language: language
    });
    setResults(prev => [response.data, ...prev].slice(0, 3));
  };
}
```

**State Management Strategy**:
- Local state for UI interactions
- Results array limited to 3 items
- Error state for user feedback

### 2. Matrix Theme System

#### Global Styles (app/globals.css)

**CSS Variables for Consistency**:
```css
:root {
  --matrix-green: #00ff00;
  --matrix-dark-green: #008800;
  --matrix-bg: #000000;
  --terminal-font: 'Courier New', monospace;
}
```

**Matrix Rain Effect**:
```css
body::before {
  content: '';
  position: fixed;
  background-image: repeating-linear-gradient(
    0deg,
    rgba(0, 255, 0, 0.03) 0px,
    transparent 1px
  );
  pointer-events: none;
}
```

#### Custom Animations

**Glitch Effect**:
```css
@keyframes glitch {
  0% {
    text-shadow: 0.05em 0 0 #00fffc,
                -0.03em -0.04em 0 #fc00ff;
  }
  50% {
    text-shadow: 0.05em 0.035em 0 #00fffc,
                0.03em 0 0 #fc00ff;
  }
}
```

**Typing Animation**:
```css
@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}
```

### 3. Component Architecture

#### CodeDisplay Component

**Purpose**: Display generated code with syntax highlighting

```typescript
export function CodeDisplay({
  code,
  language,
  title
}: CodeDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="matrix-card">
      <SyntaxHighlighter
        language={language}
        style={customMatrixTheme}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
```

**Features**:
- Syntax highlighting with custom theme
- Copy to clipboard functionality
- Download as file
- Line numbers toggle

#### MatrixLoader Component

**Purpose**: Loading states with themed animations

```typescript
export function MatrixLoader() {
  return (
    <div className="loading-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}
```

**Animation CSS**:
```css
.loading-dots span {
  animation: pulse 1.4s infinite ease-in-out;
}
```

## UI/UX Design Patterns

### 1. Form Design

**Input Components**:
```typescript
<textarea
  className="matrix-input"
  placeholder="Describe what you want to build..."
  value={prompt}
  onChange={(e) => setPrompt(e.target.value)}
/>
```

**Matrix Input Styling**:
```css
.matrix-input {
  @apply bg-black border-2 border-green-400 text-green-400
         focus:border-green-300 focus:shadow-green-400/30;
}
```

### 2. Responsive Grid Layout

```typescript
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <LanguageSelector />
  <NaturalLanguageSelector />
</div>
```

### 3. Tab Navigation

```typescript
const [activeTab, setActiveTab] = useState<'code'|'tests'|'docs'>('code');

<div className="flex gap-4 border-b border-green-400/30">
  {['code', 'tests', 'docs'].map(tab => (
    <button
      className={activeTab === tab ? 'active' : ''}
      onClick={() => setActiveTab(tab)}
    >
      {tab.toUpperCase()}
    </button>
  ))}
</div>
```

## State Management

### Local State Pattern

```typescript
interface GenerationResult {
  id: string;
  code: string;
  tests?: string;
  documentation?: string;
  metrics?: CodeMetrics;
}

const [results, setResults] = useState<GenerationResult[]>([]);
```

### Error Handling

```typescript
const [error, setError] = useState('');

try {
  const response = await axios.post(...);
} catch (err: any) {
  setError(err.response?.data?.detail || 'Generation failed');
}
```

### Loading States

```typescript
const [loading, setLoading] = useState(false);

const handleGenerate = async () => {
  setLoading(true);
  try {
    // API call
  } finally {
    setLoading(false);
  }
};
```

## API Integration

### Environment Configuration

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
```

### Request Structure

```typescript
const requestData = {
  prompt,
  programming_language: language,
  natural_language: naturalLanguage,
  project_goals: projectGoals,
  include_tests: includeTests,
  include_docs: includeDocs
};
```

### Response Handling

```typescript
const newResult: GenerationResult = {
  id: response.data.id,
  code: response.data.code,
  tests: response.data.tests?.test_code,
  documentation: response.data.documentation?.readme,
  metrics: response.data.metrics
};
```

## Performance Optimizations

### 1. Code Splitting

Next.js automatically code-splits by route:
```typescript
// Only loads when component is needed
const CodeDisplay = dynamic(() => import('@/components/CodeDisplay'));
```

### 2. Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="Logo"
  width={180}
  height={38}
  priority
/>
```

### 3. Bundle Size Reduction

```json
// package.json
{
  "dependencies": {
    // Only essential dependencies
    "react": "^18",
    "axios": "^1.6"
  }
}
```

## Styling Best Practices

### 1. Utility-First with Tailwind

```typescript
<button className="px-6 py-3 bg-transparent border-2 border-green-400">
  Generate
</button>
```

### 2. Component Classes

```css
.matrix-button {
  @apply px-6 py-3 bg-transparent border-2 border-green-400
         hover:bg-green-400 hover:text-black;
}
```

### 3. CSS-in-JS for Dynamic Styles

```typescript
const dynamicStyle = {
  color: isActive ? 'var(--matrix-green)' : 'var(--matrix-dark-green)'
};
```

## Accessibility

### 1. Semantic HTML

```typescript
<main>
  <header>
    <h1>AI Code Generator</h1>
  </header>
  <section aria-label="Input Form">
    ...
  </section>
</main>
```

### 2. Keyboard Navigation

```typescript
<button
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter') handleGenerate();
  }}
>
```

### 3. ARIA Labels

```typescript
<textarea
  aria-label="Code generation prompt"
  placeholder="Describe what you want to build..."
/>
```

## Testing Strategy

### Component Testing

```typescript
// __tests__/CodeDisplay.test.tsx
import { render, screen } from '@testing-library/react';

test('displays code with syntax highlighting', () => {
  render(<CodeDisplay code="print('hello')" language="python" />);
  expect(screen.getByText("print('hello')")).toBeInTheDocument();
});
```

### Integration Testing

```typescript
// __tests__/Dashboard.test.tsx
test('generates code on button click', async () => {
  render(<Dashboard />);

  fireEvent.change(screen.getByPlaceholderText('Describe...'), {
    target: { value: 'Create hello world' }
  });

  fireEvent.click(screen.getByText('GENERATE CODE'));

  await waitFor(() => {
    expect(screen.getByText(/Generated Code/)).toBeInTheDocument();
  });
});
```

## Development Workflow

### Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

### Environment Setup

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Common Patterns

### 1. Conditional Rendering

```typescript
{error && (
  <div className="error-message">
    {error}
  </div>
)}
```

### 2. List Rendering

```typescript
{results.map(result => (
  <ResultCard key={result.id} result={result} />
))}
```

### 3. Event Handlers

```typescript
const handleLanguageChange = (e: ChangeEvent<HTMLSelectElement>) => {
  setLanguage(e.target.value as ProgrammingLanguage);
};
```

## Troubleshooting

### Issue: CORS Errors

**Solution**: Ensure backend CORS configuration includes frontend URL
```python
# backend/config.py
cors_origins = ["http://localhost:3000"]
```

### Issue: Environment Variables Not Loading

**Solution**: Restart development server after changing `.env.local`

### Issue: Styling Not Applied

**Solution**: Ensure Tailwind content paths are correct
```javascript
// tailwind.config.ts
content: [
  './app/**/*.{js,ts,jsx,tsx}',
  './components/**/*.{js,ts,jsx,tsx}'
]
```

## Deployment

### Production Build

```bash
npm run build
```

### Environment Variables

Set in deployment platform:
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Performance Metrics

Target metrics:
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Lighthouse Score: > 90

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for streaming responses
2. **Code Editor**: Monaco editor for in-browser code editing
3. **Themes**: Multiple theme options beyond Matrix
4. **Offline Support**: Service worker for offline functionality
5. **Collaboration**: Share generated code via unique URLs
6. **History**: Save and retrieve previous generations
7. **Export Options**: Multiple format exports (PDF, Markdown)
8. **Mobile App**: React Native version