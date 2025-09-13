'use client';

import React from 'react';

export function MatrixLoader() {
  return (
    <div className="flex items-center justify-center space-x-2">
      <div className="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className="text-green-400 font-mono">PROCESSING</span>
    </div>
  );
}

export function MatrixSpinner() {
  return (
    <div className="relative w-16 h-16">
      <div className="absolute inset-0 border-2 border-green-400/30 animate-spin"></div>
      <div className="absolute inset-2 border-2 border-green-400/50 animate-spin-reverse"></div>
      <div className="absolute inset-4 border-2 border-green-400 animate-pulse"></div>
    </div>
  );
}