(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AgentSidebar",
    ()=>AgentSidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$down$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDown$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/chevron-down.js [app-client] (ecmascript) <export default as ChevronDown>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$right$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronRight$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/chevron-right.js [app-client] (ecmascript) <export default as ChevronRight>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/activity.js [app-client] (ecmascript) <export default as Activity>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle-check-big.js [app-client] (ecmascript) <export default as CheckCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/clock.js [app-client] (ecmascript) <export default as Clock>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Circle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle.js [app-client] (ecmascript) <export default as Circle>");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
const AGENT_CATEGORIES = {
    'Management & Strategy': [
        {
            name: 'Project Manager',
            role: 'Primary interface & task orchestration'
        },
        {
            name: 'Requirements Analyst',
            role: 'Requirement elicitation & refinement'
        },
        {
            name: 'System Architect',
            role: 'Technical architecture & system design'
        },
        {
            name: 'Business Analyst',
            role: 'Business objectives & value alignment'
        }
    ],
    'Design & Creative': [
        {
            name: 'UX Designer',
            role: 'User experience & interaction design'
        },
        {
            name: 'UI Designer',
            role: 'Visual aesthetics & component design'
        },
        {
            name: 'Graphics Designer',
            role: 'Visual assets & multimedia content'
        }
    ],
    'Development & Engineering': [
        {
            name: 'Backend Developer',
            role: 'Server-side logic & APIs'
        },
        {
            name: 'Frontend Developer',
            role: 'User interface implementation'
        },
        {
            name: 'Database Specialist',
            role: 'Database design & optimization'
        },
        {
            name: 'DevOps Engineer',
            role: 'Infrastructure & CI/CD'
        },
        {
            name: 'AI/ML Engineer',
            role: 'AI model integration & ML pipelines'
        },
        {
            name: 'Data Scientist',
            role: 'Data analysis & predictive models'
        },
        {
            name: 'Solution Integrator',
            role: 'System integration & APIs'
        }
    ],
    'Quality Assurance & Security': [
        {
            name: 'QA Tester',
            role: 'Testing & quality assurance'
        },
        {
            name: 'Security Auditor',
            role: 'Security assessment & compliance'
        },
        {
            name: 'Performance Engineer',
            role: 'Performance optimization'
        },
        {
            name: 'Accessibility Specialist',
            role: 'Accessibility compliance'
        }
    ],
    'Documentation & Knowledge': [
        {
            name: 'Technical Writer',
            role: 'Documentation & specifications'
        },
        {
            name: 'Knowledge Base Curator',
            role: 'RAG system management'
        },
        {
            name: 'Document Analyst',
            role: 'Document processing & analysis'
        },
        {
            name: 'Audio/Video Analyst',
            role: 'Media transcription & insights'
        }
    ],
    'System Intelligence': [
        {
            name: 'Learning Specialist',
            role: 'System learning & adaptation'
        },
        {
            name: 'Troubleshooter',
            role: 'Error diagnosis & debugging'
        }
    ]
};
const StatusIcon = (param)=>{
    let { status } = param;
    switch(status){
        case 'working':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__["Activity"], {
                className: "w-4 h-4 text-cyan-400 animate-pulse"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 56,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'complete':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__["CheckCircle"], {
                className: "w-4 h-4 text-green-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 58,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'error':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Circle$3e$__["Circle"], {
                className: "w-4 h-4 text-red-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 60,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        default:
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__["Clock"], {
                className: "w-4 h-4 text-neutral-600"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 62,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
    }
};
_c = StatusIcon;
function AgentSidebar(param) {
    let { agentStatuses = {} } = param;
    _s();
    const [expandedCategories, setExpandedCategories] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(new Set([
        'Management & Strategy',
        'Development & Engineering'
    ]));
    const toggleCategory = (category)=>{
        const newExpanded = new Set(expandedCategories);
        if (newExpanded.has(category)) {
            newExpanded.delete(category);
        } else {
            newExpanded.add(category);
        }
        setExpandedCategories(newExpanded);
    };
    const getAgentStatus = (agentName)=>{
        var _agentStatuses_agentName;
        return ((_agentStatuses_agentName = agentStatuses[agentName]) === null || _agentStatuses_agentName === void 0 ? void 0 : _agentStatuses_agentName.status) || 'idle';
    };
    const getAgentTask = (agentName)=>{
        var _agentStatuses_agentName;
        return (_agentStatuses_agentName = agentStatuses[agentName]) === null || _agentStatuses_agentName === void 0 ? void 0 : _agentStatuses_agentName.currentTask;
    };
    const getAgentProgress = (agentName)=>{
        var _agentStatuses_agentName;
        return (_agentStatuses_agentName = agentStatuses[agentName]) === null || _agentStatuses_agentName === void 0 ? void 0 : _agentStatuses_agentName.progress;
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "w-80 bg-neutral-900/50 backdrop-blur-xl border-r border-neutral-800/50 flex flex-col h-full",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-4 border-b border-neutral-800/50",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-lg font-semibold text-teal-400",
                        children: "JAi Cortex Agents"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                        lineNumber: 100,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-xs text-neutral-500 mt-1",
                        children: "24 Specialist Team Members"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                        lineNumber: 103,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 99,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 overflow-y-auto p-2 space-y-2",
                children: Object.entries(AGENT_CATEGORIES).map((param)=>{
                    let [category, agents] = param;
                    const isExpanded = expandedCategories.has(category);
                    const activeAgents = agents.filter((a)=>getAgentStatus(a.name) === 'working').length;
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-lg overflow-hidden",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>toggleCategory(category),
                                className: "w-full px-3 py-2 bg-neutral-800/50 hover:bg-neutral-800/70 transition-all flex items-center justify-between group",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center gap-2",
                                        children: [
                                            isExpanded ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$down$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDown$3e$__["ChevronDown"], {
                                                className: "w-4 h-4 text-neutral-500"
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                lineNumber: 119,
                                                columnNumber: 21
                                            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$right$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronRight$3e$__["ChevronRight"], {
                                                className: "w-4 h-4 text-neutral-500"
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                lineNumber: 121,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                className: "text-sm font-medium text-neutral-300",
                                                children: category
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                lineNumber: 123,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                        lineNumber: 117,
                                        columnNumber: 17
                                    }, this),
                                    activeAgents > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "px-2 py-0.5 bg-cyan-500/20 text-cyan-400 text-xs rounded-full",
                                        children: [
                                            activeAgents,
                                            " active"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                        lineNumber: 126,
                                        columnNumber: 19
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                lineNumber: 113,
                                columnNumber: 15
                            }, this),
                            isExpanded && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "bg-neutral-900/30 p-2 space-y-1",
                                children: agents.map((agent)=>{
                                    const status = getAgentStatus(agent.name);
                                    const task = getAgentTask(agent.name);
                                    const progress = getAgentProgress(agent.name);
                                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "p-2 rounded-xl transition-all ".concat(status === 'working' ? 'bg-cyan-500/10 border border-cyan-500/30' : status === 'complete' ? 'bg-green-500/10 border border-green-500/30' : 'bg-neutral-900/30 border border-transparent'),
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-start gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(StatusIcon, {
                                                    status: status
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                    lineNumber: 151,
                                                    columnNumber: 27
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    className: "flex-1 min-w-0",
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            className: "flex items-center justify-between gap-2",
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                                    className: "text-sm font-medium text-neutral-200 truncate",
                                                                    children: agent.name
                                                                }, void 0, false, {
                                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                                    lineNumber: 154,
                                                                    columnNumber: 31
                                                                }, this),
                                                                progress !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                    className: "text-xs text-neutral-500 whitespace-nowrap",
                                                                    children: [
                                                                        progress,
                                                                        "%"
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                                    lineNumber: 158,
                                                                    columnNumber: 33
                                                                }, this)
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                            lineNumber: 153,
                                                            columnNumber: 29
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            className: "text-xs text-neutral-600 truncate mt-0.5",
                                                            children: task || agent.role
                                                        }, void 0, false, {
                                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                            lineNumber: 163,
                                                            columnNumber: 29
                                                        }, this),
                                                        progress !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            className: "mt-1.5 h-1 bg-neutral-800 rounded-full overflow-hidden",
                                                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "h-full bg-gradient-to-r from-pink-400 to-cyan-400 transition-all duration-300",
                                                                style: {
                                                                    width: "".concat(progress, "%")
                                                                }
                                                            }, void 0, false, {
                                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                                lineNumber: 168,
                                                                columnNumber: 33
                                                            }, this)
                                                        }, void 0, false, {
                                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                            lineNumber: 167,
                                                            columnNumber: 31
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                                    lineNumber: 152,
                                                    columnNumber: 27
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                            lineNumber: 150,
                                            columnNumber: 25
                                        }, this)
                                    }, agent.name, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                        lineNumber: 140,
                                        columnNumber: 23
                                    }, this);
                                })
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                                lineNumber: 133,
                                columnNumber: 17
                            }, this)
                        ]
                    }, category, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                        lineNumber: 112,
                        columnNumber: 13
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
                lineNumber: 106,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx",
        lineNumber: 98,
        columnNumber: 5
    }, this);
}
_s(AgentSidebar, "+73z4sY2pml2x1IzjxpbIrxqUx0=");
_c1 = AgentSidebar;
var _c, _c1;
__turbopack_context__.k.register(_c, "StatusIcon");
__turbopack_context__.k.register(_c1, "AgentSidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "StatusBar",
    ()=>StatusBar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/activity.js [app-client] (ecmascript) <export default as Activity>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle-check-big.js [app-client] (ecmascript) <export default as CheckCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle-alert.js [app-client] (ecmascript) <export default as AlertCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/loader-circle.js [app-client] (ecmascript) <export default as Loader2>");
"use client";
;
;
function StatusBar(param) {
    let { currentStatus } = param;
    if (!currentStatus) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "h-12 bg-neutral-900/80 backdrop-blur-xl border-b border-neutral-800/50 px-6 flex items-center",
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-2 text-neutral-500",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__["Activity"], {
                        className: "w-4 h-4"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                        lineNumber: 17,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-sm",
                        children: "Ready to assist"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                        lineNumber: 18,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 16,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
            lineNumber: 15,
            columnNumber: 7
        }, this);
    }
    const getStatusColor = (status)=>{
        if (status.includes('complete') || status.includes('success')) {
            return 'text-green-400';
        } else if (status.includes('error') || status.includes('fail')) {
            return 'text-red-400';
        } else {
            return 'text-cyan-400';
        }
    };
    const getStatusIcon = (status)=>{
        if (status.includes('complete') || status.includes('success')) {
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__["CheckCircle"], {
                className: "w-4 h-4"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 36,
                columnNumber: 14
            }, this);
        } else if (status.includes('error') || status.includes('fail')) {
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__["AlertCircle"], {
                className: "w-4 h-4"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 38,
                columnNumber: 14
            }, this);
        } else {
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__["Loader2"], {
                className: "w-4 h-4 animate-spin"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 40,
                columnNumber: 14
            }, this);
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "h-12 bg-neutral-900/80 backdrop-blur-xl border-b border-neutral-800/50 px-6 flex items-center justify-between",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-3 ".concat(getStatusColor(currentStatus.status)),
                children: [
                    getStatusIcon(currentStatus.status),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "font-medium",
                                children: currentStatus.agent
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                                lineNumber: 49,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-neutral-600",
                                children: "•"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                                lineNumber: 50,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-sm",
                                children: currentStatus.status
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                                lineNumber: 51,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                        lineNumber: 48,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 46,
                columnNumber: 7
            }, this),
            currentStatus.progress !== undefined && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-3",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "w-48 h-2 bg-neutral-800 rounded-full overflow-hidden",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "h-full bg-gradient-to-r from-pink-400 to-cyan-400 transition-all duration-300",
                            style: {
                                width: "".concat(currentStatus.progress, "%")
                            }
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                            lineNumber: 58,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                        lineNumber: 57,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-sm font-medium ".concat(getStatusColor(currentStatus.status)),
                        children: [
                            currentStatus.progress,
                            "%"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                        lineNumber: 63,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
                lineNumber: 56,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx",
        lineNumber: 45,
        columnNumber: 5
    }, this);
}
_c = StatusBar;
var _c;
__turbopack_context__.k.register(_c, "StatusBar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "TracePanel",
    ()=>TracePanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$arrow$2d$right$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ArrowRight$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/arrow-right.js [app-client] (ecmascript) <export default as ArrowRight>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$file$2d$text$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__FileText$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/file-text.js [app-client] (ecmascript) <export default as FileText>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Code$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/code.js [app-client] (ecmascript) <export default as Code>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$database$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Database$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/database.js [app-client] (ecmascript) <export default as Database>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle-alert.js [app-client] (ecmascript) <export default as AlertCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/circle-check-big.js [app-client] (ecmascript) <export default as CheckCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/clock.js [app-client] (ecmascript) <export default as Clock>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
const EventIcon = (param)=>{
    let { type } = param;
    switch(type){
        case 'delegation':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$arrow$2d$right$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ArrowRight$3e$__["ArrowRight"], {
                className: "w-4 h-4 text-cyan-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 23,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'tool_use':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Code$3e$__["Code"], {
                className: "w-4 h-4 text-purple-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 25,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'artifact':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$file$2d$text$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__FileText$3e$__["FileText"], {
                className: "w-4 h-4 text-yellow-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 27,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'error':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__["AlertCircle"], {
                className: "w-4 h-4 text-red-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 29,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'complete':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$check$2d$big$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__CheckCircle$3e$__["CheckCircle"], {
                className: "w-4 h-4 text-green-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 31,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'status':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__["Clock"], {
                className: "w-4 h-4 text-teal-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 33,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        case 'response':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$file$2d$text$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__FileText$3e$__["FileText"], {
                className: "w-4 h-4 text-blue-400"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 35,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
        default:
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__["Clock"], {
                className: "w-4 h-4 text-neutral-500"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 37,
                columnNumber: 14
            }, ("TURBOPACK compile-time value", void 0));
    }
};
_c = EventIcon;
const EventTypeLabel = (param)=>{
    let { type } = param;
    const labels = {
        delegation: {
            text: 'Delegated',
            color: 'bg-cyan-500/20 text-cyan-400'
        },
        tool_use: {
            text: 'Tool Used',
            color: 'bg-purple-500/20 text-purple-400'
        },
        artifact: {
            text: 'Artifact',
            color: 'bg-yellow-500/20 text-yellow-400'
        },
        error: {
            text: 'Error',
            color: 'bg-red-500/20 text-red-400'
        },
        complete: {
            text: 'Complete',
            color: 'bg-green-500/20 text-green-400'
        },
        status: {
            text: 'Status',
            color: 'bg-teal-500/20 text-teal-400'
        },
        response: {
            text: 'Response',
            color: 'bg-blue-500/20 text-blue-400'
        }
    };
    const label = labels[type] || {
        text: 'Event',
        color: 'bg-gray-500/20 text-gray-400'
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: "px-2 py-0.5 rounded text-xs font-medium ".concat(label.color),
        children: label.text
    }, void 0, false, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
        lineNumber: 55,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c1 = EventTypeLabel;
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        fractionalSecondDigits: 3
    });
}
function TracePanel(param) {
    let { events } = param;
    _s();
    const scrollRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "TracePanel.useEffect": ()=>{
            if (scrollRef.current) {
                scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
            }
        }
    }["TracePanel.useEffect"], [
        events
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "w-96 bg-neutral-900/50 backdrop-blur-xl border-l border-neutral-800/50 flex flex-col h-full",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-4 border-b border-neutral-800/50",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-lg font-semibold text-teal-400",
                        children: "Agent Trace"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                        lineNumber: 84,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-xs text-neutral-500 mt-1",
                        children: "Real-time collaboration flow"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                        lineNumber: 87,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 83,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                ref: scrollRef,
                className: "flex-1 overflow-y-auto p-4 space-y-3",
                children: events.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex flex-col items-center justify-center h-full text-neutral-500",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$clock$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Clock$3e$__["Clock"], {
                            className: "w-12 h-12 mb-2 opacity-50"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                            lineNumber: 93,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-sm",
                            children: "No activity yet"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                            lineNumber: 94,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-xs text-neutral-600 mt-1",
                            children: "Agent collaboration will appear here"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                            lineNumber: 95,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                    lineNumber: 92,
                    columnNumber: 11
                }, this) : events.map((event)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "bg-neutral-800/50 rounded-lg p-3 border border-neutral-700/50 hover:border-neutral-600/50 transition-all",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-start gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "mt-0.5",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(EventIcon, {
                                        type: event.type
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                        lineNumber: 105,
                                        columnNumber: 19
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                    lineNumber: 104,
                                    columnNumber: 17
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex-1 min-w-0",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-center gap-2 mb-1",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(EventTypeLabel, {
                                                    type: event.type
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 109,
                                                    columnNumber: 21
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-xs text-neutral-500",
                                                    children: formatTime(event.timestamp)
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 110,
                                                    columnNumber: 21
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 108,
                                            columnNumber: 19
                                        }, this),
                                        event.fromAgent && event.toAgent && event.type === 'delegation' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-center gap-2 text-sm mb-1",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "font-medium text-neutral-300",
                                                    children: event.fromAgent
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 117,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$arrow$2d$right$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ArrowRight$3e$__["ArrowRight"], {
                                                    className: "w-3 h-3 text-neutral-500"
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 118,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "font-medium text-neutral-300",
                                                    children: event.toAgent
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 119,
                                                    columnNumber: 23
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 116,
                                            columnNumber: 21
                                        }, this),
                                        event.fromAgent && !event.toAgent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-sm font-medium text-neutral-300 mb-1",
                                            children: event.fromAgent
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 124,
                                            columnNumber: 21
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-sm text-neutral-400",
                                            children: event.action
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 129,
                                            columnNumber: 19
                                        }, this),
                                        event.details && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-xs text-neutral-500 mt-1 font-mono bg-neutral-950/50 p-1.5 rounded break-all",
                                            children: event.details
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 132,
                                            columnNumber: 21
                                        }, this),
                                        event.artifact && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "mt-2 flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/30 rounded p-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$database$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Database$3e$__["Database"], {
                                                    className: "w-4 h-4 text-yellow-400"
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 139,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    className: "flex-1 min-w-0",
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            className: "text-xs text-yellow-400 font-medium truncate",
                                                            children: event.artifact.name
                                                        }, void 0, false, {
                                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                            lineNumber: 141,
                                                            columnNumber: 25
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            className: "text-xs text-neutral-500",
                                                            children: event.artifact.type
                                                        }, void 0, false, {
                                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                            lineNumber: 144,
                                                            columnNumber: 25
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                                    lineNumber: 140,
                                                    columnNumber: 23
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                            lineNumber: 138,
                                            columnNumber: 21
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                                    lineNumber: 107,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                            lineNumber: 103,
                            columnNumber: 15
                        }, this)
                    }, event.id, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                        lineNumber: 99,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
                lineNumber: 90,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx",
        lineNumber: 82,
        columnNumber: 5
    }, this);
}
_s(TracePanel, "P14GFulhWAl/Oec4Pk4QeBwKyr0=");
_c2 = TracePanel;
var _c, _c1, _c2;
__turbopack_context__.k.register(_c, "EventIcon");
__turbopack_context__.k.register(_c1, "EventTypeLabel");
__turbopack_context__.k.register(_c2, "TracePanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>ChatPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/styled-jsx/style.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$send$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Send$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/send.js [app-client] (ecmascript) <export default as Send>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Mic$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic.js [app-client] (ecmascript) <export default as Mic>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2d$off$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__MicOff$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic-off.js [app-client] (ecmascript) <export default as MicOff>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$AgentSidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/AgentSidebar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$StatusBar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/StatusBar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$TracePanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/TracePanel.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
;
;
function ChatPage() {
    _s();
    const [messages, setMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([
        {
            id: '1',
            role: 'assistant',
            content: "Hello! I'm JAi Cortex - your 24-agent development team. I have specialists for every aspect of software development. What would you like to build today?",
            timestamp: Date.now(),
            agent: 'Project Manager'
        }
    ]);
    const [input, setInput] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [agentStatuses, setAgentStatuses] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({});
    const [currentStatus, setCurrentStatus] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])();
    const [traceEvents, setTraceEvents] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [isRecording, setIsRecording] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const messagesEndRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const scrollToBottom = ()=>{
        var _messagesEndRef_current;
        (_messagesEndRef_current = messagesEndRef.current) === null || _messagesEndRef_current === void 0 ? void 0 : _messagesEndRef_current.scrollIntoView({
            behavior: 'smooth'
        });
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatPage.useEffect": ()=>{
            scrollToBottom();
        }
    }["ChatPage.useEffect"], [
        messages
    ]);
    const handleSend = async ()=>{
        if (!input.trim() || isLoading) return;
        const startTime = Date.now(); // Start timer
        const userMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: Date.now()
        };
        setMessages((prev)=>[
                ...prev,
                userMessage
            ]);
        const messageToSend = input;
        setInput('');
        setIsLoading(true);
        // Add loading indicator message
        const loadingId = 'loading-' + Date.now();
        setMessages((prev)=>[
                ...prev,
                {
                    id: loadingId,
                    role: 'assistant',
                    content: '⏳ JAi Cortex is thinking...',
                    timestamp: Date.now()
                }
            ]);
        // Add trace for user message
        setTraceEvents((prev)=>[
                ...prev,
                {
                    id: "user-msg-".concat(Date.now(), "-").concat(Math.random()),
                    timestamp: Date.now(),
                    type: 'message',
                    fromAgent: 'User',
                    action: 'Message sent',
                    details: messageToSend.substring(0, 100)
                }
            ]);
        try {
            // Use local JAi Cortex OS backend with complete ADK system
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: messageToSend,
                    session_id: 'main-session',
                    user_id: 'default'
                })
            });
            const data = await response.json();
            const responseTime = ((Date.now() - startTime) / 1000).toFixed(2); // Calculate response time in seconds
            // Add tool calls to trace (if any)
            if (data.tool_calls && data.tool_calls.length > 0) {
                data.tool_calls.forEach((toolCall)=>{
                    setTraceEvents((prev)=>[
                            ...prev,
                            {
                                id: "tool-".concat(Date.now(), "-").concat(Math.random()),
                                timestamp: Date.now(),
                                type: 'tool_use',
                                fromAgent: 'JAi Cortex',
                                action: "Tool: ".concat(toolCall.name),
                                details: JSON.stringify(toolCall.args, null, 2)
                            }
                        ]);
                });
            }
            // ALWAYS add response trace with timing
            setTraceEvents((prev)=>[
                    ...prev,
                    {
                        id: "response-".concat(Date.now(), "-").concat(Math.random()),
                        timestamp: Date.now(),
                        type: 'response',
                        fromAgent: 'JAi Cortex',
                        action: "Response generated in ".concat(responseTime, "s"),
                        details: data.response.substring(0, 150) + (data.response.length > 150 ? '...' : '')
                    }
                ]);
            // Remove loading message and add real response
            setMessages((prev)=>{
                const filtered = prev.filter((m)=>m.id !== loadingId);
                return [
                    ...filtered,
                    {
                        id: (Date.now() + 1).toString(),
                        role: 'assistant',
                        content: data.response,
                        timestamp: Date.now()
                    }
                ];
            });
            setIsLoading(false);
        } catch (error) {
            console.error('Error:', error);
            const errorTime = ((Date.now() - startTime) / 1000).toFixed(2);
            // Remove loading message and show error
            setMessages((prev)=>{
                const filtered = prev.filter((m)=>m.id !== loadingId);
                return [
                    ...filtered,
                    {
                        id: (Date.now() + 1).toString(),
                        role: 'assistant',
                        content: '❌ Sorry, I encountered an error. Please try again.',
                        timestamp: Date.now()
                    }
                ];
            });
            // Add error trace with timing
            setTraceEvents((prev)=>[
                    ...prev,
                    {
                        id: "trace-error-".concat(Date.now(), "-").concat(Math.random()),
                        timestamp: Date.now(),
                        type: 'error',
                        fromAgent: 'System',
                        action: "Request failed after ".concat(errorTime, "s"),
                        details: error instanceof Error ? error.message : 'Unknown error'
                    }
                ]);
        } finally{
            setIsLoading(false);
        }
    };
    const toggleRecording = ()=>{
        setIsRecording(!isRecording);
    // Voice recording logic would go here
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "jsx-48d09f8361f3e339" + " " + "flex h-screen w-full bg-neutral-950 relative overflow-hidden",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "jsx-48d09f8361f3e339" + " " + "absolute inset-0 pointer-events-none",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-96 h-96 bg-teal-500/20 rounded-full blur-3xl animate-float-slow top-0 -left-20"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 170,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-80 h-80 bg-teal-400/15 rounded-full blur-3xl animate-float-medium bottom-20 right-10"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 171,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-72 h-72 bg-sky-400/20 rounded-full blur-3xl animate-float-medium top-40 right-0"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 174,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-64 h-64 bg-blue-500/15 rounded-full blur-3xl animate-float-slow bottom-0 left-1/3"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 175,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-60 h-60 bg-pink-400/10 rounded-full blur-3xl animate-float-fast top-1/3 left-1/4"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 178,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "absolute w-56 h-56 bg-pink-500/15 rounded-full blur-3xl animate-float-medium bottom-40 right-1/4"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 179,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                lineNumber: 168,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$AgentSidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AgentSidebar"], {
                agentStatuses: agentStatuses
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                lineNumber: 183,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "jsx-48d09f8361f3e339" + " " + "flex-1 flex flex-col",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$StatusBar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["StatusBar"], {
                        currentStatus: currentStatus
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 188,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "flex-1 overflow-y-auto p-6 space-y-4",
                        children: [
                            messages.map((message)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "jsx-48d09f8361f3e339" + " " + "flex ".concat(message.role === 'user' ? 'justify-end' : 'justify-start'),
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "jsx-48d09f8361f3e339" + " " + "max-w-xl rounded-2xl px-4 py-3 ".concat(message.role === 'user' ? 'bg-teal-500/20 border border-teal-400/40' : 'bg-neutral-800/50 border border-neutral-700/50'),
                                        children: [
                                            message.agent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "jsx-48d09f8361f3e339" + " " + "text-xs font-medium text-cyan-400 mb-2",
                                                children: message.agent
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                                lineNumber: 205,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "jsx-48d09f8361f3e339" + " " + "text-gray-100 whitespace-pre-wrap",
                                                children: message.content
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                                lineNumber: 209,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                suppressHydrationWarning: true,
                                                className: "jsx-48d09f8361f3e339" + " " + "text-xs text-gray-500 mt-2",
                                                children: new Date(message.timestamp).toLocaleTimeString()
                                            }, void 0, false, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                                lineNumber: 210,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                        lineNumber: 197,
                                        columnNumber: 15
                                    }, this)
                                }, message.id, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                    lineNumber: 193,
                                    columnNumber: 13
                                }, this)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                ref: messagesEndRef,
                                className: "jsx-48d09f8361f3e339"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                lineNumber: 216,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 191,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "jsx-48d09f8361f3e339" + " " + "border-t border-neutral-800/50 bg-neutral-900/80 backdrop-blur-xl p-4",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "jsx-48d09f8361f3e339" + " " + "flex items-end gap-3",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: toggleRecording,
                                    className: "jsx-48d09f8361f3e339" + " " + "p-3 rounded-xl transition-all ".concat(isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-neutral-800 hover:bg-neutral-700'),
                                    children: isRecording ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2d$off$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__MicOff$3e$__["MicOff"], {
                                        className: "w-5 h-5 text-white"
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                        lineNumber: 231,
                                        columnNumber: 17
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Mic$3e$__["Mic"], {
                                        className: "w-5 h-5 text-white"
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                        lineNumber: 233,
                                        columnNumber: 17
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                    lineNumber: 222,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "jsx-48d09f8361f3e339" + " " + "flex-1",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                                        value: input,
                                        onChange: (e)=>setInput(e.target.value),
                                        onKeyDown: (e)=>{
                                            if (e.key === 'Enter' && !e.shiftKey) {
                                                e.preventDefault();
                                                handleSend();
                                            }
                                        },
                                        placeholder: "Describe what you want to build...",
                                        rows: 1,
                                        style: {
                                            minHeight: '48px',
                                            maxHeight: '120px'
                                        },
                                        className: "jsx-48d09f8361f3e339" + " " + "w-full bg-neutral-900/50 border border-neutral-800/50 rounded-xl px-4 py-3 text-gray-100 placeholder-neutral-500 focus:outline-none focus:border-cyan-400/50 resize-none"
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                        lineNumber: 238,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                    lineNumber: 237,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: handleSend,
                                    disabled: isLoading || !input.trim(),
                                    className: "jsx-48d09f8361f3e339" + " " + "p-3 bg-sky-400 hover:bg-sky-500 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-sky-500/20",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$send$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Send$3e$__["Send"], {
                                        className: "w-5 h-5 text-white"
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                        lineNumber: 259,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                                    lineNumber: 254,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                            lineNumber: 221,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                        lineNumber: 220,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                lineNumber: 186,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$TracePanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TracePanel"], {
                events: traceEvents
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
                lineNumber: 266,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                id: "48d09f8361f3e339",
                children: "@keyframes float-slow{0%,to{transform:translate(0)scale(1)}33%{transform:translate(30px,-40px)scale(1.1)}66%{transform:translate(-20px,40px)scale(.9)}}@keyframes float-medium{0%,to{transform:translate(0)scale(1)}50%{transform:translate(-40px,-50px)scale(1.15)}}@keyframes float-fast{0%,to{transform:translate(0)scale(1)}25%{transform:translate(50px,30px)scale(.95)}75%{transform:translate(-30px,-40px)scale(1.05)}}.animate-float-slow.jsx-48d09f8361f3e339{animation:20s ease-in-out infinite float-slow}.animate-float-medium.jsx-48d09f8361f3e339{animation:15s ease-in-out infinite float-medium}.animate-float-fast.jsx-48d09f8361f3e339{animation:12s ease-in-out infinite float-fast}"
            }, void 0, false, void 0, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/chat/page.tsx",
        lineNumber: 166,
        columnNumber: 5
    }, this);
}
_s(ChatPage, "kACsSs8DBY61lbgCQh7IOw6YDaI=");
_c = ChatPage;
var _c;
__turbopack_context__.k.register(_c, "ChatPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=Agent%20master%20_genesis-agent_cortex-chat-ui_src_e0f5ad73._.js.map