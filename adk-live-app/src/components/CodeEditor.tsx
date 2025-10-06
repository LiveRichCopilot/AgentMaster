import { Editor } from '@monaco-editor/react';
import { motion } from 'framer-motion';
import { useState } from 'react';

interface CodeEditorProps {
  code: string;
  language: string;
  onChange: (value: string) => void;
  onRun: () => void;
  output?: string;
  error?: string;
  isRunning: boolean;
}

export const CodeEditor = ({ code, language, onChange, onRun, output, error, isRunning }: CodeEditorProps) => {
  const [showPreview, setShowPreview] = useState(true);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl overflow-hidden flex flex-col h-[600px]"
    >
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-black/20">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/60"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/60"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/60"></div>
          </div>
          <span className="text-white/60 text-sm font-mono">{language}</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 bg-white/5 hover:bg-white/10 text-white/60"
          >
            {showPreview ? 'Hide' : 'Show'} Preview
          </button>
          <button
            onClick={onRun}
            disabled={isRunning}
            className="px-4 py-1.5 rounded-lg text-sm font-medium transition-all duration-300 bg-teal-500/20 hover:bg-teal-500/30 text-teal-400 shadow-lg shadow-teal-500/10 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isRunning ? (
              <>
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Running...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
                Run Code
              </>
            )}
          </button>
        </div>
      </div>

      <div className="flex-1 flex">
        <div className={`${showPreview ? 'w-1/2' : 'w-full'} transition-all duration-300`}>
          <Editor
            height="100%"
            language={language}
            value={code}
            onChange={(value) => onChange(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 2,
              wordWrap: 'on',
              padding: { top: 16, bottom: 16 },
              cursorStyle: 'line',
              cursorBlinking: 'smooth',
              smoothScrolling: true,
              fontFamily: "'Fira Code', 'Monaco', 'Menlo', monospace",
              fontLigatures: true,
            }}
          />
        </div>

        {showPreview && (
          <div className="w-1/2 border-l border-white/10 flex flex-col bg-black/30">
            <div className="px-4 py-2 border-b border-white/10 bg-black/20">
              <span className="text-white/60 text-sm font-medium">Output</span>
            </div>
            <div className="flex-1 overflow-auto p-4">
              {error ? (
                <div className="glass rounded-lg p-4 border-l-4 border-red-500 bg-red-500/10">
                  <div className="text-red-400 text-sm font-semibold mb-2">Error</div>
                  <pre className="text-red-300/90 text-sm font-mono whitespace-pre-wrap">{error}</pre>
                </div>
              ) : output ? (
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">{output}</pre>
              ) : (
                <div className="text-white/40 text-sm text-center py-8">
                  Click "Run Code" to see output
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};
