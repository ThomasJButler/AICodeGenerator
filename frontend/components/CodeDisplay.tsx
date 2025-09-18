'use client';

import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check, Download, Maximize2 } from 'lucide-react';

interface CodeDisplayProps {
  code: string;
  language: string;
  title?: string;
  showLineNumbers?: boolean;
}

export function CodeDisplay({
  code,
  language,
  title = 'Generated Code',
  showLineNumbers = true
}: CodeDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const extension = getFileExtension(language);
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `generated_code.${extension}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="glass-effect rounded-lg overflow-hidden">
      <div className="flex justify-between items-center p-4 bg-card border-b border-glass">
        <h3 className="text-matrix font-medium text-sm flex items-center">
          <span className="bg-matrix text-black px-2 py-1 rounded text-xs font-semibold mr-2">
            {language.toUpperCase()}
          </span>
          {title}
        </h3>
        <div className="flex space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 rounded-lg hover:bg-matrix/10 transition-all duration-200 interactive"
            title="Copy code"
          >
            {copied ? (
              <Check className="w-4 h-4 text-success" />
            ) : (
              <Copy className="w-4 h-4 text-matrix" />
            )}
          </button>
          <button
            onClick={handleDownload}
            className="p-2 rounded-lg hover:bg-matrix/10 transition-all duration-200 interactive"
            title="Download code"
          >
            <Download className="w-4 h-4 text-matrix" />
          </button>
        </div>
      </div>

      <div className="relative">
        <SyntaxHighlighter
          language={language}
          style={{
            ...atomDark,
            'pre[class*="language-"]': {
              ...atomDark['pre[class*="language-"]'],
              background: 'var(--deep-black)',
              border: 'none',
              padding: '1.5rem',
              fontSize: '0.875rem',
              fontFamily: 'var(--font-mono)',
              lineHeight: '1.6',
            },
            'code[class*="language-"]': {
              ...atomDark['code[class*="language-"]'],
              background: 'var(--deep-black)',
              color: 'var(--text-primary)',
            },
            'token.keyword': {
              color: 'var(--matrix-green)',
            },
            'token.string': {
              color: 'var(--matrix-cyan)',
            },
            'token.function': {
              color: '#ff6b6b',
            },
            'token.number': {
              color: '#feca57',
            },
            'token.comment': {
              color: 'var(--text-muted)',
              fontStyle: 'italic',
            }
          }}
          showLineNumbers={showLineNumbers}
          customStyle={{
            background: 'var(--deep-black)',
            margin: 0,
            maxHeight: '600px',
            overflow: 'auto',
            borderRadius: '0 0 12px 12px',
          }}
          lineNumberStyle={{
            color: 'var(--text-muted)',
            backgroundColor: 'transparent',
            paddingRight: '1rem',
            borderRight: '1px solid var(--glass-border)',
            marginRight: '1rem',
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}

function getFileExtension(language: string): string {
  const extensions: Record<string, string> = {
    python: 'py',
    javascript: 'js',
    typescript: 'ts',
    java: 'java',
    csharp: 'cs',
    go: 'go',
    rust: 'rs',
    cpp: 'cpp',
    ruby: 'rb',
    swift: 'swift'
  };
  return extensions[language.toLowerCase()] || 'txt';
}