"use client";

import { ArrowRight, FileText, Code, Database, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { useEffect, useRef } from 'react';

export interface TraceEvent {
  id: string;
  timestamp: number;
  type: 'delegation' | 'tool_use' | 'artifact' | 'error' | 'complete' | 'status' | 'response';
  fromAgent?: string;
  toAgent?: string;
  action: string;
  details?: string;
  artifact?: {
    type: string;
    name: string;
  };
}

const EventIcon = ({ type }: { type: TraceEvent['type'] }) => {
  switch (type) {
    case 'delegation':
      return <ArrowRight className="w-4 h-4 text-cyan-400" />;
    case 'tool_use':
      return <Code className="w-4 h-4 text-purple-400" />;
    case 'artifact':
      return <FileText className="w-4 h-4 text-yellow-400" />;
    case 'error':
      return <AlertCircle className="w-4 h-4 text-red-400" />;
    case 'complete':
      return <CheckCircle className="w-4 h-4 text-green-400" />;
    case 'status':
      return <Clock className="w-4 h-4 text-teal-400" />;
    case 'response':
      return <FileText className="w-4 h-4 text-blue-400" />;
    default:
      return <Clock className="w-4 h-4 text-neutral-500" />;
  }
};

const EventTypeLabel = ({ type }: { type: TraceEvent['type'] }) => {
  const labels = {
    delegation: { text: 'Delegated', color: 'bg-cyan-500/20 text-cyan-400' },
    tool_use: { text: 'Tool Used', color: 'bg-purple-500/20 text-purple-400' },
    artifact: { text: 'Artifact', color: 'bg-yellow-500/20 text-yellow-400' },
    error: { text: 'Error', color: 'bg-red-500/20 text-red-400' },
    complete: { text: 'Complete', color: 'bg-green-500/20 text-green-400' },
    status: { text: 'Status', color: 'bg-teal-500/20 text-teal-400' },
    response: { text: 'Response', color: 'bg-blue-500/20 text-blue-400' },
  };

  const label = labels[type] || { text: 'Event', color: 'bg-gray-500/20 text-gray-400' };

  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${label.color}`}>
      {label.text}
    </span>
  );
};

function formatTime(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour12: false, 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit',
    fractionalSecondDigits: 3 
  });
}

export function TracePanel({ events }: { events: TraceEvent[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="w-96 bg-neutral-900/50 backdrop-blur-xl border-l border-neutral-800/50 flex flex-col h-full">
      <div className="p-4 border-b border-neutral-800/50">
        <h2 className="text-lg font-semibold text-teal-400">
          Agent Trace
        </h2>
        <p className="text-xs text-neutral-500 mt-1">Real-time collaboration flow</p>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
        {events.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-neutral-500">
            <Clock className="w-12 h-12 mb-2 opacity-50" />
            <p className="text-sm">No activity yet</p>
            <p className="text-xs text-neutral-600 mt-1">Agent collaboration will appear here</p>
          </div>
        ) : (
          events.map((event) => (
            <div
              key={event.id}
              className="bg-neutral-800/50 rounded-lg p-3 border border-neutral-700/50 hover:border-neutral-600/50 transition-all"
            >
              <div className="flex items-start gap-2">
                <div className="mt-0.5">
                  <EventIcon type={event.type} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <EventTypeLabel type={event.type} />
                    <span className="text-xs text-neutral-500">
                      {formatTime(event.timestamp)}
                    </span>
                  </div>

                  {event.fromAgent && event.toAgent && event.type === 'delegation' && (
                    <div className="flex items-center gap-2 text-sm mb-1">
                      <span className="font-medium text-neutral-300">{event.fromAgent}</span>
                      <ArrowRight className="w-3 h-3 text-neutral-500" />
                      <span className="font-medium text-neutral-300">{event.toAgent}</span>
                    </div>
                  )}

                  {event.fromAgent && !event.toAgent && (
                    <div className="text-sm font-medium text-neutral-300 mb-1">
                      {event.fromAgent}
                    </div>
                  )}

                  <p className="text-sm text-neutral-400">{event.action}</p>

                  {event.details && (
                    <p className="text-xs text-neutral-500 mt-1 font-mono bg-neutral-950/50 p-1.5 rounded break-all">
                      {event.details}
                    </p>
                  )}

                  {event.artifact && (
                    <div className="mt-2 flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/30 rounded p-2">
                      <Database className="w-4 h-4 text-yellow-400" />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs text-yellow-400 font-medium truncate">
                          {event.artifact.name}
                        </p>
                        <p className="text-xs text-neutral-500">
                          {event.artifact.type}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
