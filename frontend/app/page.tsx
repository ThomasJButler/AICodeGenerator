'use client';

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { Terminal, Code, FileText, TestTube, Sparkles, ArrowLeft, ExternalLink, Github, HelpCircle } from 'lucide-react';
import { CodeDisplay } from '@/components/CodeDisplay';
import { MatrixLoader } from '@/components/MatrixLoader';
import { ProgressBar } from '@/components/ProgressBar';
import { Notification } from '@/components/Notification';
import { Footer } from '@/components/Footer';
import { HowItWorksModal } from '@/components/HowItWorksModal';
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
  const [showNotification, setShowNotification] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');
  const [showHowItWorks, setShowHowItWorks] = useState(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  const funnyStatusMessages = useMemo(() => [
    'Flibbertigibberting the algorithms...',
    'Reticulating splines...',
    'Optimizing quantum flux capacitors...',
    'Teaching electrons to dance...',
    'Herding digital cats...',
    'Calibrating the coffee machine...',
    'Convincing bits to behave...',
    'Shuffling bytes around...',
    'Tickling the transistors...',
    'Whispering to the compiler...',
    'Feeding the code gremlins...',
    'Polishing the pixels...',
    'Debugging the debugger...',
    'Summoning the syntax spirits...',
    'Organizing chaos into order...',
    'Negotiating with the API overlords...',
    'Bribing the syntax checker...',
    'Teaching AI to be creative...',
    'Untangling spaghetti code...',
    'Convincing the server to cooperate...',
    'Channeling the spirit of Turing...',
    'Asking Stack Overflow for help...',
    'Performing digital alchemy...',
    'Consulting the coding oracle...',
    'Translating human thoughts to machine...',
    'Optimizing the hamster wheels...',
    'Defragmenting the neural networks...',
    'Calibrating the chaos engine...',
    'Synchronizing with the matrix...',
    'Awakening the dormant algorithms...',
    'Brewing the perfect code blend...',
    'Polishing the logic diamonds...',
    'Tuning the frequency of brilliance...',
    'Assembling the digital symphony...',
    'Weaving the fabric of functionality...'
  ], []);

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

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        if (!loading && prompt.trim()) {
          handleGenerate();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [loading, prompt]); // eslint-disable-line react-hooks/exhaustive-deps

  // Smooth scroll to results after generation
  useEffect(() => {
    if (results.length > 0 && resultsRef.current) {
      resultsRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }, [results.length]);

  const handleGenerate = useCallback(async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');
    setProgress(0);
    setStatusMessage(funnyStatusMessages[0]);

    // Simulate progress updates with funny status messages
    let messageIndex = 0;
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) return prev;
        return prev + Math.random() * 7; // Slower progress increments
      });
    }, 1500); // Slower progress updates

    const messageInterval = setInterval(() => {
      messageIndex = (messageIndex + 1) % funnyStatusMessages.length;
      setStatusMessage(funnyStatusMessages[messageIndex]);
    }, 5000); // Change message every 5 seconds

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

      clearInterval(progressInterval);
      clearInterval(messageInterval);
      setProgress(100);
      setStatusMessage('Code generation complete!');

      const newResult: GenerationResult = {
        id: response.data.id,
        code: response.data.code,
        tests: response.data.tests?.test_code,
        documentation: response.data.documentation?.readme,
        language: response.data.language,
        metrics: response.data.metrics
      };

      setResults(prev => [newResult, ...prev].slice(0, 3));
      setShowNotification(true);

      // Reset form
      setPrompt('');
      setProjectGoals('');
    } catch (err: unknown) {
      clearInterval(progressInterval);
      clearInterval(messageInterval);
      setProgress(0);
      setStatusMessage('');
      const errorMessage = err instanceof Error
        ? err.message
        : (err && typeof err === 'object' && 'response' in err && err.response && typeof err.response === 'object' && 'data' in err.response && err.response.data && typeof err.response.data === 'object' && 'detail' in err.response.data)
          ? String(err.response.data.detail)
          : 'Generation failed. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
      setTimeout(() => {
        setProgress(0);
        setStatusMessage('');
      }, 2000);
    }
  }, [prompt, language, naturalLanguage, projectGoals, includeTests, includeDocs, funnyStatusMessages]);

  return (
    <div className="min-h-screen relative z-10">
      {/* Navigation Header */}
      <nav className="p-4 md:p-6 border-b border-glass">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <a
            href="https://www.aitomatic.io/"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary flex items-center space-x-2 min-h-[44px]"
            title="Back to Portfolio"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Back to Portfolio</span>
          </a>

          <div className="flex items-center space-x-2 sm:space-x-4">
            <button
              onClick={() => setShowHowItWorks(true)}
              className="btn-secondary flex items-center space-x-2 min-h-[44px]"
              title="How It Works"
            >
              <HelpCircle className="w-4 h-4" />
              <span className="hidden sm:inline">How It Works</span>
            </button>

            <a
              href="https://github.com/ThomasJButler/AICodeGenerator"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary flex items-center space-x-2 min-h-[44px]"
              title="GitHub Repository"
            >
              <Github className="w-4 h-4" />
              <span className="hidden sm:inline">GitHub Repo</span>
              <ExternalLink className="w-4 h-4 hidden sm:inline" />
            </a>
          </div>
        </div>
      </nav>

      <div className="p-4 md:p-8">
        {/* Header */}
        <header className="mb-12 text-center animate-fade-in">
        <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-primary mb-4 text-matrix">
          AI CODE GENERATOR
        </h1>
        <p className="text-secondary text-base sm:text-lg md:text-xl max-w-2xl mx-auto">
          Generate production-ready code with AI assistance
        </p>
      </header>

      {/* Section Divider */}
      <div className="section-divider section-divider-animated"></div>

      {/* Main Input Section */}
      <div className="max-w-6xl mx-auto">
        <div className="glass-card animate-scale-in">
          <div className="grid gap-8">
            {/* Prompt Input */}
            <div>
              <label className="block text-matrix text-sm font-medium mb-3 flex items-center">
                <Terminal className="w-4 h-4 mr-2" />
                Describe what you want to build
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="glass-input w-full h-32 resize-none focus-ring"
                placeholder="Example: Create a function that calculates fibonacci numbers with memoization..."
              />
            </div>

            {/* Language Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <label className="block text-matrix text-sm font-medium mb-3 flex items-center">
                  <Code className="w-4 h-4 mr-2" />
                  Programming Language
                </label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="glass-select w-full focus-ring"
                >
                  {programmingLanguages.map(lang => (
                    <option key={lang.value} value={lang.value}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-matrix text-sm font-medium mb-3 flex items-center">
                  <FileText className="w-4 h-4 mr-2" />
                  Natural Language
                </label>
                <select
                  value={naturalLanguage}
                  onChange={(e) => setNaturalLanguage(e.target.value)}
                  className="glass-select w-full focus-ring"
                >
                  <option value="english">English</option>
                  <option value="spanish">Spanish</option>
                  <option value="french">French</option>
                  <option value="german">German</option>
                  <option value="chinese">Chinese (Mandarin)</option>
                </select>
              </div>
            </div>

            {/* Project Goals */}
            <div>
              <label className="block text-matrix text-sm font-medium mb-3 flex items-center">
                <Sparkles className="w-4 h-4 mr-2" />
                Project Goals (Optional)
              </label>
              <input
                type="text"
                value={projectGoals}
                onChange={(e) => setProjectGoals(e.target.value)}
                className="glass-input w-full focus-ring"
                placeholder="Build efficient mathematical utilities..."
              />
            </div>

            {/* Options */}
            <div className="flex flex-col sm:flex-row gap-4 sm:gap-8">
              <label className="flex items-center text-secondary cursor-pointer interactive min-h-[44px]">
                <input
                  type="checkbox"
                  checked={includeTests}
                  onChange={(e) => setIncludeTests(e.target.checked)}
                  className="mr-3 w-5 h-5 text-matrix bg-transparent border-glass rounded focus:ring-matrix"
                />
                <TestTube className="w-4 h-4 mr-2" />
                <span className="text-sm sm:text-base">Generate Tests</span>
              </label>
              <label className="flex items-center text-secondary cursor-pointer interactive min-h-[44px]">
                <input
                  type="checkbox"
                  checked={includeDocs}
                  onChange={(e) => setIncludeDocs(e.target.checked)}
                  className="mr-3 w-5 h-5 text-matrix bg-transparent border-glass rounded focus:ring-matrix"
                />
                <FileText className="w-4 h-4 mr-2" />
                <span className="text-sm sm:text-base">Generate Documentation</span>
              </label>
            </div>

            {/* Error Display */}
            {error && (
              <div className="error-alert">
                <strong>Error:</strong> {error}
              </div>
            )}

            {/* Progress Bar */}
            {loading && (
              <div className="animate-fade-in">
                <ProgressBar progress={progress} statusMessage={statusMessage} />
              </div>
            )}

            {/* Generate Button */}
            <div className="space-y-2">
              <button
                onClick={handleGenerate}
                disabled={loading}
                className={`btn-primary w-full ${loading ? 'loading' : ''}`}
              >
                {loading ? <MatrixLoader /> : 'Generate Code'}
              </button>
              <p className="text-xs text-muted text-center">
                Press <kbd className="px-2 py-1 bg-glass-bg border border-glass rounded text-matrix">⌘ + Enter</kbd> or <kbd className="px-2 py-1 bg-glass-bg border border-glass rounded text-matrix">Ctrl + Enter</kbd> to generate
              </p>
            </div>
          </div>
        </div>
      </div>

        {/* Results Section */}
        {results.length > 0 && (
          <>
            {/* Section Divider */}
            <div className="section-divider"></div>

            <div ref={resultsRef} className="space-y-8 animate-fade-in">
              <h2 className="text-3xl font-bold text-matrix mb-6">
                Generated Results
              </h2>

              {results.map((result, index) => (
                <div key={result.id} className="glass-card animate-scale-in" style={{ animationDelay: `${index * 100}ms` }}>
                  {/* Tab Navigation with Result Counter */}
                  <div className="flex justify-between items-center p-4 border-b border-glass">
                    <div className="tab-nav">
                      <button
                        onClick={() => setActiveTab('code')}
                        className={`tab-button ${activeTab === 'code' ? 'active' : ''}`}
                      >
                        Code
                      </button>
                      {result.tests && (
                        <button
                          onClick={() => setActiveTab('tests')}
                          className={`tab-button ${activeTab === 'tests' ? 'active' : ''}`}
                        >
                          Tests
                        </button>
                      )}
                      {result.documentation && (
                        <button
                          onClick={() => setActiveTab('docs')}
                          className={`tab-button ${activeTab === 'docs' ? 'active' : ''}`}
                        >
                          Documentation
                        </button>
                      )}
                    </div>
                    <div className="text-sm text-secondary">
                      Result <span className="text-matrix font-semibold">{index + 1}</span>/{results.length}
                    </div>
                  </div>

                {/* Tab Content */}
                {activeTab === 'code' && (
                  <div className="tab-content">
                    <CodeDisplay
                      code={result.code}
                      language={result.language}
                      title="Generated Code"
                    />
                    {result.metrics && (
                      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="glass-effect p-4 rounded-lg text-center">
                          <div className="text-muted text-sm">Lines of Code</div>
                          <div className="text-matrix text-xl font-semibold">{result.metrics.lines_of_code}</div>
                        </div>
                        <div className="glass-effect p-4 rounded-lg text-center">
                          <div className="text-muted text-sm">Complexity</div>
                          <div className="text-matrix text-xl font-semibold">{result.metrics.cyclomatic_complexity}</div>
                        </div>
                        <div className="glass-effect p-4 rounded-lg text-center">
                          <div className="text-muted text-sm">Readability</div>
                          <div className="text-matrix text-xl font-semibold">{result.metrics.readability_score}%</div>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'tests' && result.tests && (
                  <div className="tab-content">
                    <CodeDisplay
                      code={result.tests}
                      language={result.language}
                      title="Unit Tests"
                    />
                  </div>
                )}

                {activeTab === 'docs' && result.documentation && (
                  <div className="tab-content">
                    <div className="glass-effect p-6 rounded-lg">
                      <pre className="text-secondary font-mono text-sm whitespace-pre-wrap leading-relaxed">
                        {result.documentation}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            ))}
            </div>
          </>
        )}

        {/* Success Notification */}
        {showNotification && (
          <Notification
            type="success"
            message="Code generated successfully!"
            onClose={() => setShowNotification(false)}
          />
        )}
      </div>

      {/* How It Works Modal */}
      <HowItWorksModal
        isOpen={showHowItWorks}
        onClose={() => setShowHowItWorks(false)}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}