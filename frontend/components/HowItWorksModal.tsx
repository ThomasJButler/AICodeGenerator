'use client';

import React from 'react';
import { Modal } from './Modal';
import { Bot, Zap, Building, Sparkles } from 'lucide-react';

interface HowItWorksModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function HowItWorksModal({ isOpen, onClose }: HowItWorksModalProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="How It Works">
      <div className="space-y-6">
        {/* AI Generation Section */}
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-matrix/20">
              <Bot className="w-6 h-6 text-matrix" />
            </div>
            <h3 className="text-xl font-semibold text-primary">AI-Powered Generation</h3>
          </div>
          <div className="pl-11 space-y-2">
            <p>• Built with GPT-4o and advanced prompt engineering techniques</p>
            <p>• Employs context-aware code completion strategies for optimal results</p>
            <p>• Generates production-ready code following industry best practices</p>
            <p>• Supports multiple programming languages with framework-specific templates</p>
          </div>
        </div>

        {/* Technology Stack Section */}
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-matrix/20">
              <Zap className="w-6 h-6 text-matrix" />
            </div>
            <h3 className="text-xl font-semibold text-primary">Technology Stack</h3>
          </div>
          <div className="pl-11 space-y-2">
            <p>• <strong>Frontend:</strong> Next.js 15 with TypeScript and Tailwind CSS</p>
            <p>• <strong>Backend:</strong> FastAPI with async processing and RESTful design</p>
            <p>• <strong>AI Orchestration:</strong> LangChain for prompt management and model interaction</p>
            <p>• <strong>Code Analysis:</strong> Tree-sitter for AST parsing and syntax validation</p>
          </div>
        </div>

        {/* Generation Pipeline Section */}
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-matrix/20">
              <Building className="w-6 h-6 text-matrix" />
            </div>
            <h3 className="text-xl font-semibold text-primary">Generation Pipeline</h3>
          </div>
          <div className="pl-11 space-y-2">
            <p>• Advanced prompt engineering with context injection and template management</p>
            <p>• Multi-step generation process with iterative refinement</p>
            <p>• Real-time streaming for immediate user feedback and progress tracking</p>
            <p>• Automated test case and documentation generation alongside code</p>
          </div>
        </div>

        {/* Code Quality Section */}
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-matrix/20">
              <Sparkles className="w-6 h-6 text-matrix" />
            </div>
            <h3 className="text-xl font-semibold text-primary">Quality & Analysis</h3>
          </div>
          <div className="pl-11 space-y-2">
            <p>• Cyclomatic complexity analysis for maintainable code structure</p>
            <p>• Automated readability scoring with industry-standard metrics</p>
            <p>• Design pattern integration for scalable architecture</p>
            <p>• Syntax highlighting with language-specific optimisation</p>
          </div>
        </div>

        {/* Learning Outcomes */}
        <div className="mt-8 p-4 rounded-lg bg-matrix/10 border border-matrix/20">
          <h4 className="text-sm font-semibold text-matrix mb-2">Key Learning Outcomes</h4>
          <p className="text-sm text-muted">
            This project demonstrates advanced prompt engineering, multi-language generation strategies,
            AST parsing techniques, and performance optimisation for real-time AI applications.
          </p>
        </div>
      </div>
    </Modal>
  );
}