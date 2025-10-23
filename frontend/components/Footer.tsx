/**
 * @author Tom Butler
 * @date 2025-10-23
 * @description Footer component with copyright, social links, and branding.
 */
'use client';

import React from 'react';
import { Github, Linkedin, Heart } from 'lucide-react';

/**
 * @return {JSX.Element}
 * @constructor
 */
export function Footer() {
  return (
    <footer className="mt-16 py-8 border-t border-glass">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="text-sm text-secondary">
            © 2025{' '}
            <a
              href="https://thomasjbutler.me"
              target="_blank"
              rel="noopener noreferrer"
              className="text-matrix hover:text-cyan transition-colors duration-200 font-medium"
            >
              Tom Butler
            </a>
            . All rights reserved.
          </div>

          {/* Made with love */}
          <div className="flex items-center text-sm text-secondary">
            Made with <Heart className="w-4 h-4 mx-1 text-error" fill="currentColor" /> for the AI community
          </div>

          {/* Social Links */}
          <div className="flex items-center space-x-4">
            <a
              href="https://github.com/ThomasJButler"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg hover:bg-matrix/10 transition-all duration-200 interactive"
              title="GitHub"
            >
              <Github className="w-5 h-5 text-matrix" />
            </a>
            <a
              href="https://www.linkedin.com/in/thomasbutleruk/"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg hover:bg-matrix/10 transition-all duration-200 interactive"
              title="LinkedIn"
            >
              <Linkedin className="w-5 h-5 text-matrix" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}