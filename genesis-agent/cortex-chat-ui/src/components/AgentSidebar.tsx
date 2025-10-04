"use client";

import { useState } from 'react';
import { ChevronDown, ChevronRight, Activity, CheckCircle, Clock, Circle } from 'lucide-react';

export interface AgentStatus {
  name: string;
  role: string;
  status: 'idle' | 'working' | 'complete' | 'error';
  currentTask?: string;
  progress?: number;
}

const AGENT_CATEGORIES = {
  'Management & Strategy': [
    { name: 'Project Manager', role: 'Primary interface & task orchestration' },
    { name: 'Requirements Analyst', role: 'Requirement elicitation & refinement' },
    { name: 'System Architect', role: 'Technical architecture & system design' },
    { name: 'Business Analyst', role: 'Business objectives & value alignment' },
  ],
  'Design & Creative': [
    { name: 'UX Designer', role: 'User experience & interaction design' },
    { name: 'UI Designer', role: 'Visual aesthetics & component design' },
    { name: 'Graphics Designer', role: 'Visual assets & multimedia content' },
  ],
  'Development & Engineering': [
    { name: 'Backend Developer', role: 'Server-side logic & APIs' },
    { name: 'Frontend Developer', role: 'User interface implementation' },
    { name: 'Database Specialist', role: 'Database design & optimization' },
    { name: 'DevOps Engineer', role: 'Infrastructure & CI/CD' },
    { name: 'AI/ML Engineer', role: 'AI model integration & ML pipelines' },
    { name: 'Data Scientist', role: 'Data analysis & predictive models' },
    { name: 'Solution Integrator', role: 'System integration & APIs' },
  ],
  'Quality Assurance & Security': [
    { name: 'QA Tester', role: 'Testing & quality assurance' },
    { name: 'Security Auditor', role: 'Security assessment & compliance' },
    { name: 'Performance Engineer', role: 'Performance optimization' },
    { name: 'Accessibility Specialist', role: 'Accessibility compliance' },
  ],
  'Documentation & Knowledge': [
    { name: 'Technical Writer', role: 'Documentation & specifications' },
    { name: 'Knowledge Base Curator', role: 'RAG system management' },
    { name: 'Document Analyst', role: 'Document processing & analysis' },
    { name: 'Audio/Video Analyst', role: 'Media transcription & insights' },
  ],
  'System Intelligence': [
    { name: 'Learning Specialist', role: 'System learning & adaptation' },
    { name: 'Troubleshooter', role: 'Error diagnosis & debugging' },
  ],
};

const StatusIcon = ({ status }: { status: AgentStatus['status'] }) => {
  switch (status) {
    case 'working':
      return <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />;
    case 'complete':
      return <CheckCircle className="w-4 h-4 text-green-400" />;
    case 'error':
      return <Circle className="w-4 h-4 text-red-400" />;
    default:
      return <Clock className="w-4 h-4 text-neutral-600" />;
  }
};

export function AgentSidebar({ 
  agentStatuses = {} 
}: { 
  agentStatuses?: Record<string, AgentStatus> 
}) {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    new Set(['Management & Strategy', 'Development & Engineering'])
  );

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const getAgentStatus = (agentName: string): AgentStatus['status'] => {
    return agentStatuses[agentName]?.status || 'idle';
  };

  const getAgentTask = (agentName: string): string | undefined => {
    return agentStatuses[agentName]?.currentTask;
  };

  const getAgentProgress = (agentName: string): number | undefined => {
    return agentStatuses[agentName]?.progress;
  };

  return (
    <div className="w-80 bg-neutral-900/50 backdrop-blur-xl border-r border-neutral-800/50 flex flex-col h-full">
      <div className="p-4 border-b border-neutral-800/50">
        <h2 className="text-lg font-semibold text-teal-400">
          JAi Cortex Agents
        </h2>
        <p className="text-xs text-neutral-500 mt-1">24 Specialist Team Members</p>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {Object.entries(AGENT_CATEGORIES).map(([category, agents]) => {
          const isExpanded = expandedCategories.has(category);
          const activeAgents = agents.filter(a => getAgentStatus(a.name) === 'working').length;
          
          return (
            <div key={category} className="rounded-lg overflow-hidden">
              <button
                onClick={() => toggleCategory(category)}
                className="w-full px-3 py-2 bg-neutral-800/50 hover:bg-neutral-800/70 transition-all flex items-center justify-between group"
              >
                <div className="flex items-center gap-2">
                  {isExpanded ? (
                    <ChevronDown className="w-4 h-4 text-neutral-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-neutral-500" />
                  )}
                  <span className="text-sm font-medium text-neutral-300">{category}</span>
                </div>
                  {activeAgents > 0 && (
                  <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 text-xs rounded-full">
                    {activeAgents} active
                  </span>
                )}
              </button>

              {isExpanded && (
                <div className="bg-neutral-900/30 p-2 space-y-1">
                  {agents.map((agent) => {
                    const status = getAgentStatus(agent.name);
                    const task = getAgentTask(agent.name);
                    const progress = getAgentProgress(agent.name);

                    return (
                      <div
                        key={agent.name}
                        className={`p-2 rounded-xl transition-all ${
                          status === 'working' 
                            ? 'bg-cyan-500/10 border border-cyan-500/30' 
                            : status === 'complete'
                            ? 'bg-green-500/10 border border-green-500/30'
                            : 'bg-neutral-900/30 border border-transparent'
                        }`}
                      >
                        <div className="flex items-start gap-2">
                          <StatusIcon status={status} />
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between gap-2">
                              <h3 className="text-sm font-medium text-neutral-200 truncate">
                                {agent.name}
                              </h3>
                              {progress !== undefined && (
                                <span className="text-xs text-neutral-500 whitespace-nowrap">
                                  {progress}%
                                </span>
                              )}
                            </div>
                            <p className="text-xs text-neutral-600 truncate mt-0.5">
                              {task || agent.role}
                            </p>
                            {progress !== undefined && (
                              <div className="mt-1.5 h-1 bg-neutral-800 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-pink-400 to-cyan-400 transition-all duration-300"
                                  style={{ width: `${progress}%` }}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
