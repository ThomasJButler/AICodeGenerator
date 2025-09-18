'use client';

import React from 'react';

interface ProgressBarProps {
  progress: number; // 0-100
  className?: string;
  showText?: boolean;
  statusMessage?: string;
}

export function ProgressBar({ progress, className = '', showText = true, statusMessage }: ProgressBarProps) {
  const clampedProgress = Math.max(0, Math.min(100, progress));

  return (
    <div className={`space-y-2 ${className}`}>
      {showText && (
        <div className="flex justify-between items-center text-sm">
          <span className="text-secondary animate-pulse">
            {statusMessage || 'Generating code...'}
          </span>
          <span className="text-matrix font-medium">{clampedProgress.toFixed(2)}%</span>
        </div>
      )}
      <div className="progress-bar">
        <div
          className="h-full bg-gradient-to-r from-matrix to-cyan rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
    </div>
  );
}