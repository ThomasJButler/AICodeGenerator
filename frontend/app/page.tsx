'use client';

import React, { useState } from 'react';
import { Terminal, Code, FileText, TestTube, Sparkles } from 'lucide-react';
import { CodeDisplay } from '@/components/CodeDisplay';
import { MatrixLoader } from '@/components/MatrixLoader';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface GenerationResult {
  id: string;
  code: string;
  tests?: string;
  documentation?: string;
  language: string;
  metrics?: {
    lines_of_code: number;
    cyclomatic_complexity: number;
    readability_score: number;
  };
}

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [language, setLanguage] = useState('python');
  const [naturalLanguage, setNaturalLanguage] = useState('english');
  const [projectGoals, setProjectGoals] = useState('');
  const [includeTests, setIncludeTests] = useState(true);
  const [includeDocs, setIncludeDocs] = useState(true);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<GenerationResult[]>([]);
  const [activeTab, setActiveTab] = useState<'code' | 'tests' | 'docs'>('code');
  const [error, setError] = useState('');

  const programmingLanguages = [
    { value: 'python', label: 'Python' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'typescript', label: 'TypeScript' },
    { value: 'java', label: 'Java' },
    { value: 'csharp', label: 'C#' },
    { value: 'go', label: 'Go' },
    { value: 'rust', label: 'Rust' },
    { value: 'cpp', label: 'C++' },
    { value: 'ruby', label: 'Ruby' },
    { value: 'swift', label: 'Swift' }
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/generate`, {
        prompt,
        programming_language: language,
        natural_language: naturalLanguage,
        project_goals: projectGoals,
        include_tests: includeTests,
        include_docs: includeDocs,
        complexity_level: 'intermediate'
      });

      const newResult: GenerationResult = {
        id: response.data.id,
        code: response.data.code,
        tests: response.data.tests?.test_code,
        documentation: response.data.documentation?.readme,
        language: response.data.language,
        metrics: response.data.metrics
      };

      setResults(prev => [newResult, ...prev].slice(0, 3));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Generation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 relative z-10">
      {/* Header */}
      <header className="mb-12 text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-green-400 mb-4 animate-glitch">
          AI CODE GENERATOR
        </h1>
        <p className="text-green-400/70 font-mono animate-typing">
          Generate production-ready code with AI assistance
        </p>
      </header>

      {/* Main Input Section */}
      <div className="max-w-6xl mx-auto">
        <div className="matrix-card p-6 mb-8">
          <div className="grid gap-4">
            {/* Prompt Input */}
            <div>
              <label className="block text-green-400 text-sm font-mono mb-2 uppercase">
                <Terminal className="inline w-4 h-4 mr-2" />
                Describe what you want to build
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="matrix-input w-full h-32 resize-none"
                placeholder="Example: Create a function that calculates fibonacci numbers with memoization..."
              />
            </div>

            {/* Language Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-green-400 text-sm font-mono mb-2 uppercase">
                  <Code className="inline w-4 h-4 mr-2" />
                  Programming Language
                </label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="matrix-input w-full"
                >
                  {programmingLanguages.map(lang => (
                    <option key={lang.value} value={lang.value}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-green-400 text-sm font-mono mb-2 uppercase">
                  <FileText className="inline w-4 h-4 mr-2" />
                  Natural Language
                </label>
                <select
                  value={naturalLanguage}
                  onChange={(e) => setNaturalLanguage(e.target.value)}
                  className="matrix-input w-full"
                >
                  <option value="english">English</option>
                  <option value="spanish">Spanish</option>
                  <option value="french">French</option>
                  <option value="german">German</option>
                  <option value="chinese">Chinese</option>
                </select>
              </div>
            </div>

            {/* Project Goals */}
            <div>
              <label className="block text-green-400 text-sm font-mono mb-2 uppercase">
                <Sparkles className="inline w-4 h-4 mr-2" />
                Project Goals (Optional)
              </label>
              <input
                type="text"
                value={projectGoals}
                onChange={(e) => setProjectGoals(e.target.value)}
                className="matrix-input w-full"
                placeholder="Build efficient mathematical utilities..."
              />
            </div>

            {/* Options */}
            <div className="flex gap-6">
              <label className="flex items-center text-green-400 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeTests}
                  onChange={(e) => setIncludeTests(e.target.checked)}
                  className="mr-2 accent-green-400"
                />
                <TestTube className="inline w-4 h-4 mr-1" />
                Generate Tests
              </label>
              <label className="flex items-center text-green-400 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeDocs}
                  onChange={(e) => setIncludeDocs(e.target.checked)}
                  className="mr-2 accent-green-400"
                />
                <FileText className="inline w-4 h-4 mr-1" />
                Generate Documentation
              </label>
            </div>

            {/* Error Display */}
            {error && (
              <div className="text-red-400 font-mono text-sm border border-red-400/30 p-2 bg-red-900/10">
                ERROR: {error}
              </div>
            )}

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="matrix-button"
            >
              {loading ? <MatrixLoader /> : 'GENERATE CODE'}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-green-400 mb-4">
              GENERATED RESULTS [{results.length}/3]
            </h2>

            {results.map((result, index) => (
              <div key={result.id} className="matrix-card p-6">
                {/* Tab Navigation */}
                <div className="flex gap-4 mb-4 border-b border-green-400/30">
                  <button
                    onClick={() => setActiveTab('code')}
                    className={`pb-2 px-4 font-mono text-sm uppercase transition-colors ${
                      activeTab === 'code'
                        ? 'text-green-400 border-b-2 border-green-400'
                        : 'text-green-400/50 hover:text-green-400/70'
                    }`}
                  >
                    Code
                  </button>
                  {result.tests && (
                    <button
                      onClick={() => setActiveTab('tests')}
                      className={`pb-2 px-4 font-mono text-sm uppercase transition-colors ${
                        activeTab === 'tests'
                          ? 'text-green-400 border-b-2 border-green-400'
                          : 'text-green-400/50 hover:text-green-400/70'
                      }`}
                    >
                      Tests
                    </button>
                  )}
                  {result.documentation && (
                    <button
                      onClick={() => setActiveTab('docs')}
                      className={`pb-2 px-4 font-mono text-sm uppercase transition-colors ${
                        activeTab === 'docs'
                          ? 'text-green-400 border-b-2 border-green-400'
                          : 'text-green-400/50 hover:text-green-400/70'
                      }`}
                    >
                      Docs
                    </button>
                  )}
                </div>

                {/* Tab Content */}
                {activeTab === 'code' && (
                  <div>
                    <CodeDisplay
                      code={result.code}
                      language={result.language}
                      title="Generated Code"
                    />
                    {result.metrics && (
                      <div className="mt-4 grid grid-cols-3 gap-4 text-sm font-mono">
                        <div className="text-green-400/70">
                          Lines: <span className="text-green-400">{result.metrics.lines_of_code}</span>
                        </div>
                        <div className="text-green-400/70">
                          Complexity: <span className="text-green-400">{result.metrics.cyclomatic_complexity}</span>
                        </div>
                        <div className="text-green-400/70">
                          Readability: <span className="text-green-400">{result.metrics.readability_score}%</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'tests' && result.tests && (
                  <CodeDisplay
                    code={result.tests}
                    language={result.language}
                    title="Unit Tests"
                  />
                )}

                {activeTab === 'docs' && result.documentation && (
                  <div className="code-block">
                    <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap">
                      {result.documentation}
                    </pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}