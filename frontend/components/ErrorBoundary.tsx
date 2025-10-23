/**
 * @author Tom Butler
 * @date 2025-10-23
 * @description React error boundary for graceful error handling.
 *              Catches errors in component tree and displays user-friendly fallback UI.
 */
'use client';

import React, { Component, ReactNode, ErrorInfo } from 'react';
import { AlertTriangle, RefreshCcw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * Error boundary component that catches React errors and prevents white screen.
 *
 * @class ErrorBoundary
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('Error boundary caught error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  handleReset = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  handleGoHome = (): void => {
    window.location.href = '/';
  };

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-deep-black p-4">
          <div className="glass-card max-w-2xl w-full">
            <div className="flex flex-col items-center text-center space-y-6">
              <div className="p-4 bg-error/10 rounded-full">
                <AlertTriangle className="w-12 h-12 text-error" />
              </div>

              <div>
                <h1 className="text-3xl font-bold text-matrix mb-2">Something went wrong</h1>
                <p className="text-secondary">
                  We encountered an unexpected error. This has been logged and we'll look into it.
                </p>
              </div>

              {process.env.NODE_ENV === 'development' && this.state.error && (
                <div className="w-full p-4 bg-black/50 rounded-lg border border-glass overflow-x-auto">
                  <pre className="text-xs text-error text-left font-mono">
                    {this.state.error.toString()}
                    {this.state.errorInfo?.componentStack}
                  </pre>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                <button
                  onClick={this.handleReset}
                  className="btn-primary flex items-center justify-center space-x-2"
                >
                  <RefreshCcw className="w-4 h-4" />
                  <span>Try Again</span>
                </button>
                <button
                  onClick={this.handleGoHome}
                  className="btn-secondary flex items-center justify-center space-x-2"
                >
                  <Home className="w-4 h-4" />
                  <span>Go Home</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
