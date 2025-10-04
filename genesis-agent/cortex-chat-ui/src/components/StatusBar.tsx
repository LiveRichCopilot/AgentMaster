"use client";

import { Activity, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

export interface StatusUpdate {
  agent: string;
  status: string;
  progress?: number;
  timestamp: number;
}

export function StatusBar({ currentStatus }: { currentStatus?: StatusUpdate }) {
  if (!currentStatus) {
    return (
      <div className="h-12 bg-neutral-900/80 backdrop-blur-xl border-b border-neutral-800/50 px-6 flex items-center">
        <div className="flex items-center gap-2 text-neutral-500">
          <Activity className="w-4 h-4" />
          <span className="text-sm">Ready to assist</span>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    if (status.includes('complete') || status.includes('success')) {
      return 'text-green-400';
    } else if (status.includes('error') || status.includes('fail')) {
      return 'text-red-400';
    } else {
      return 'text-cyan-400';
    }
  };

  const getStatusIcon = (status: string) => {
    if (status.includes('complete') || status.includes('success')) {
      return <CheckCircle className="w-4 h-4" />;
    } else if (status.includes('error') || status.includes('fail')) {
      return <AlertCircle className="w-4 h-4" />;
    } else {
      return <Loader2 className="w-4 h-4 animate-spin" />;
    }
  };

  return (
    <div className="h-12 bg-neutral-900/80 backdrop-blur-xl border-b border-neutral-800/50 px-6 flex items-center justify-between">
      <div className={`flex items-center gap-3 ${getStatusColor(currentStatus.status)}`}>
        {getStatusIcon(currentStatus.status)}
        <div className="flex items-center gap-2">
          <span className="font-medium">{currentStatus.agent}</span>
          <span className="text-neutral-600">•</span>
          <span className="text-sm">{currentStatus.status}</span>
        </div>
      </div>

      {currentStatus.progress !== undefined && (
        <div className="flex items-center gap-3">
          <div className="w-48 h-2 bg-neutral-800 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-pink-400 to-cyan-400 transition-all duration-300"
              style={{ width: `${currentStatus.progress}%` }}
            />
          </div>
          <span className={`text-sm font-medium ${getStatusColor(currentStatus.status)}`}>
            {currentStatus.progress}%
          </span>
        </div>
      )}
    </div>
  );
}
