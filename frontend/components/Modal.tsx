'use client';

import React, { useEffect } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm animate-fade-in"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl mx-4 animate-scale-in">
        <div className="glass-card max-h-[80vh] overflow-y-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-6 pb-4 border-b border-glass">
            <h2 className="text-2xl font-bold text-matrix">{title}</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-matrix/10 transition-all duration-200 interactive"
              title="Close modal"
            >
              <X className="w-5 h-5 text-matrix" />
            </button>
          </div>

          {/* Content */}
          <div className="text-secondary">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}