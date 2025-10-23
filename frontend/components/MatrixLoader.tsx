/**
 * @author Tom Butler
 * @date 2025-10-23
 * @description Matrix-themed loading animations.
 *              Provides pulsing dots and spinning loader variants.
 */
'use client';

import React from 'react';

/**
 * @return {JSX.Element}
 * @constructor
 */
export function MatrixLoader() {
  return (
    <div className="flex items-center justify-center space-x-3">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-matrix rounded-full animate-pulse" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-matrix rounded-full animate-pulse" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-matrix rounded-full animate-pulse" style={{ animationDelay: '300ms' }}></div>
      </div>
      <span className="text-matrix font-medium text-sm">Processing...</span>
    </div>
  );
}

export function MatrixSpinner() {
  return (
    <div className="relative w-16 h-16">
      <div className="absolute inset-0 border-2 border-matrix/30 rounded-full animate-spin"></div>
      <div className="absolute inset-2 border-2 border-matrix/60 rounded-full animate-spin" style={{ animationDirection: 'reverse' }}></div>
      <div className="absolute inset-4 border-2 border-matrix rounded-full animate-pulse"></div>
    </div>
  );
}