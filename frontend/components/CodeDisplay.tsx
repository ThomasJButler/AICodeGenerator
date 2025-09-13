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
    <div className="matrix-card p-4">
      <div className="flex justify-between items-center mb-4 border-b border-green-400/30 pb-2">
        <h3 className="text-green-400 font-mono text-sm uppercase tracking-wider">
          {title} [{language.toUpperCase()}]
        </h3>
        <div className="flex space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 hover:bg-green-400/10 transition-colors"
            title="Copy code"
          >
            {copied ? (
              <Check className="w-4 h-4 text-green-400" />
            ) : (
              <Copy className="w-4 h-4 text-green-400" />
            )}
          </button>
          <button
            onClick={handleDownload}
            className="p-2 hover:bg-green-400/10 transition-colors"
            title="Download code"
          >
            <Download className="w-4 h-4 text-green-400" />
          </button>
        </div>
      </div>

      <div className="relative">
        <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-green-400 to-transparent opacity-50"></div>
        <SyntaxHighlighter
          language={language}
          style={{
            ...atomDark,
            'pre[class*="language-"]': {
              ...atomDark['pre[class*="language-"]'],
              background: '#000000',
              border: '1px solid rgba(0, 255, 0, 0.2)',
              padding: '1rem',
              fontSize: '0.875rem',
              fontFamily: 'Courier New, monospace',
            },
            'code[class*="language-"]': {
              ...atomDark['code[class*="language-"]'],
              background: '#000000',
              color: '#00ff00',
            }
          }}
          showLineNumbers={showLineNumbers}
          customStyle={{
            background: '#000000',
            margin: 0,
            maxHeight: '500px',
            overflow: 'auto'
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