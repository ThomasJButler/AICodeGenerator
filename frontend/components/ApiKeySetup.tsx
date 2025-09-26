'use client';

import React, { useState, useEffect } from 'react';
import { Key, Eye, EyeOff, CheckCircle, AlertCircle, ExternalLink, Shield, Lock } from 'lucide-react';

interface ApiKeySetupProps {
  onApiKeySet: (apiKey: string) => void;
  onSkip?: () => void;
  showSkip?: boolean;
}

export function ApiKeySetup({ onApiKeySet, onSkip, showSkip = false }: ApiKeySetupProps) {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState<'idle' | 'valid' | 'invalid' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    // Check if there's already an API key stored
    const storedKey = localStorage.getItem('openai_api_key');
    if (storedKey) {
      setApiKey(storedKey);
      validateApiKey(storedKey);
    }
  }, []);

  const validateApiKey = async (key: string) => {
    if (!key.trim()) {
      setValidationStatus('idle');
      return;
    }

    setIsValidating(true);
    setValidationStatus('idle');
    setErrorMessage('');

    try {
      const response = await fetch('https://api.openai.com/v1/models', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${key.trim()}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setValidationStatus('valid');
        localStorage.setItem('openai_api_key', key.trim());
      } else if (response.status === 401) {
        setValidationStatus('invalid');
        setErrorMessage('Invalid API key. Please check your key and try again.');
      } else if (response.status === 429) {
        setValidationStatus('error');
        setErrorMessage('Rate limit exceeded. Please try again later.');
      } else {
        setValidationStatus('error');
        setErrorMessage('Unable to validate API key. Please try again.');
      }
    } catch {
      setValidationStatus('error');
      setErrorMessage('Network error. Please check your connection and try again.');
    } finally {
      setIsValidating(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validationStatus === 'valid' && apiKey.trim()) {
      onApiKeySet(apiKey.trim());
    } else {
      validateApiKey(apiKey);
    }
  };

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setApiKey(value);
    setValidationStatus('idle');
    setErrorMessage('');
  };

  const getValidationIcon = () => {
    if (isValidating) {
      return <div className="w-5 h-5 border-2 border-matrix border-t-transparent rounded-full animate-spin" />;
    }

    switch (validationStatus) {
      case 'valid':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'invalid':
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-400" />;
      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-lg mx-auto animate-scale-in">
      <div className="glass-card w-full">
        <div className="text-center mb-6">
          <div className="flex justify-center mb-3">
            <div className="p-2 bg-matrix/20 rounded-full">
              <Key className="w-6 h-6 text-matrix" />
            </div>
          </div>
          <h1 className="text-2xl md:text-3xl font-bold text-matrix mb-2">Setup OpenAI API Key</h1>
          <p className="text-secondary text-sm md:text-base">
            To generate code, you&apos;ll need to provide your own OpenAI API key
          </p>
        </div>

        {/* Security Information */}
        <div className="glass-effect p-4 md:p-6 rounded-lg mb-6">
          <div className="flex items-start space-x-3 mb-4">
            <Shield className="w-5 h-5 text-matrix mt-1 flex-shrink-0" />
            <div>
              <h3 className="text-matrix font-semibold mb-2">Your Privacy & Security</h3>
              <ul className="text-secondary text-sm space-y-1">
                <li className="flex items-center space-x-2">
                  <Lock className="w-3 h-3" />
                  <span>Your API key is stored locally in your browser</span>
                </li>
                <li className="flex items-center space-x-2">
                  <Lock className="w-3 h-3" />
                  <span>We never see or store your API key on our servers</span>
                </li>
                <li className="flex items-center space-x-2">
                  <Lock className="w-3 h-3" />
                  <span>All requests go directly from your browser to OpenAI</span>
                </li>
                <li className="flex items-center space-x-2">
                  <Lock className="w-3 h-3" />
                  <span>You can remove your key anytime from settings</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 md:space-y-6">
          <div>
            <label className="block text-matrix text-sm font-medium mb-3">
              OpenAI API Key
            </label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={handleApiKeyChange}
                className={`glass-input w-full pr-20 focus-ring ${
                  validationStatus === 'valid' ? 'border-green-400' :
                  validationStatus === 'invalid' || validationStatus === 'error' ? 'border-red-400' :
                  'border-glass'
                }`}
                placeholder="sk-..."
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center space-x-1 pr-3">
                {getValidationIcon()}
                <button
                  type="button"
                  onClick={() => setShowKey(!showKey)}
                  className="p-1 text-secondary hover:text-matrix transition-colors"
                >
                  {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            {errorMessage && (
              <p className="text-red-400 text-sm mt-2 flex items-center space-x-1">
                <AlertCircle className="w-4 h-4" />
                <span>{errorMessage}</span>
              </p>
            )}
          </div>

          <div className="space-y-4">
            <button
              type="submit"
              disabled={isValidating || (!apiKey.trim())}
              className={`btn-primary w-full ${isValidating || !apiKey.trim() ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isValidating ? 'Validating...' : validationStatus === 'valid' ? 'Continue' : 'Validate & Continue'}
            </button>

            {showSkip && onSkip && (
              <button
                type="button"
                onClick={onSkip}
                className="btn-secondary w-full"
              >
                Skip for now
              </button>
            )}
          </div>
        </form>

        {/* Help Section */}
        <div className="mt-6 md:mt-8 pt-4 md:pt-6 border-t border-glass">
          <h3 className="text-matrix font-semibold mb-3">Need an OpenAI API Key?</h3>
          <div className="space-y-3 text-sm text-secondary">
            <div className="flex items-start space-x-2">
              <span className="text-matrix font-medium">1.</span>
              <div>
                <span>Visit </span>
                <a
                  href="https://platform.openai.com/api-keys"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-matrix hover:underline inline-flex items-center space-x-1"
                >
                  <span>OpenAI Platform</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
                <span> and sign in</span>
              </div>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-matrix font-medium">2.</span>
              <span>Click &quot;Create new secret key&quot; and copy it</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-matrix font-medium">3.</span>
              <span>Paste it above and start generating code!</span>
            </div>
          </div>
          <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <p className="text-xs text-yellow-300">
              <strong>Note:</strong> You&apos;ll need to add payment information to your OpenAI account.
              API usage is pay-per-use and typically costs just a few cents per generation.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}