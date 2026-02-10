// src/app/war-room/page.tsx
'use client';

import { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icons } from '@/components/Icons';

type Log = {
    timestamp: string;
    agent: string; // LOGIC_CORE, EMPATHY_ENGINE, ETHICS_VALIDATOR
    log: string;
    status: string;
};

export default function WarRoom() {
    const [logs, setLogs] = useState<Log[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);
    const [riskLevel, setRiskLevel] = useState(12);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        // Try WebSocket connection, fall back to mock data if unavailable
        let ws: WebSocket | null = null;
        let mockInterval: NodeJS.Timeout | null = null;

        try {
            ws = new WebSocket('ws://localhost:8000/api/war_room/ws');

            ws.onopen = () => {
                setConnected(true);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                setLogs((prev) => [...prev.slice(-99), data]);

                if (data.agent === 'ETHICS_VALIDATOR' && data.status === 'BLOCKED') {
                    setRiskLevel(prev => Math.min(prev + 5, 95));
                } else if (data.status === 'SAFE') {
                    setRiskLevel(prev => Math.max(prev - 1, 5));
                }
            };

            ws.onerror = () => {
                setConnected(false);
                initializeMockData();
            };
        } catch (error) {
            setConnected(false);
            initializeMockData();
        }

        function initializeMockData() {
            // Simulate logs when backend is unavailable
            const mockAgents = ['LOGIC_CORE', 'EMPATHY_ENGINE', 'ETHICS_VALIDATOR'];
            const mockStatuses = ['PROCESSING', 'SAFE', 'ANALYZING', 'BLOCKED'];
            const mockLogs = [
                "Evaluating decision tree for user request...",
                "Analyzing emotional impact on stakeholders",
                "Verifying alignment with constitutional principles",
                "Cross-referencing against established precedents",
                "Simulating long-term consequences",
                "Checking for potential bias in data sources",
                "Assessing transparency requirements"
            ];

            mockInterval = setInterval(() => {
                const newLog: Log = {
                    timestamp: new Date().toISOString(),
                    agent: mockAgents[Math.floor(Math.random() * mockAgents.length)],
                    log: mockLogs[Math.floor(Math.random() * mockLogs.length)],
                    status: mockStatuses[Math.floor(Math.random() * mockStatuses.length)]
                };

                setLogs((prev) => [...prev.slice(-99), newLog]);

                if (newLog.status === 'BLOCKED') {
                    setRiskLevel(prev => Math.min(prev + 3, 85));
                } else {
                    setRiskLevel(prev => Math.max(prev - 0.5, 5));
                }
            }, 2000);
        }

        return () => {
            if (ws) ws.close();
            if (mockInterval) clearInterval(mockInterval);
        };
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="min-h-screen p-4 sm:p-6 lg:p-8 bg-gradient-to-br from-black via-green-900/5 to-black text-white font-mono">
            <div className="max-w-7xl mx-auto h-[calc(100vh-2rem)] sm:h-[calc(100vh-3rem)] lg:h-[calc(100vh-4rem)] flex flex-col space-y-4 sm:space-y-6">

                {/* Header & Risk Meter */}
                <motion.div
                    className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-green-500/20 pb-4 sm:pb-6 gap-4"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <div className="flex items-center space-x-3 sm:space-x-4">
                        <motion.div
                            className="p-2.5 sm:p-3 bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-lg border border-green-500/40 backdrop-blur-sm shadow-[0_0_20px_rgba(34,197,94,0.2)]"
                            animate={{
                                boxShadow: [
                                    "0_0_20px_rgba(34,197,94,0.2)",
                                    "0_0_30px_rgba(34,197,94,0.4)",
                                    "0_0_20px_rgba(34,197,94,0.2)"
                                ]
                            }}
                            transition={{ duration: 2, repeat: Infinity }}
                        >
                            <Icons.WarRoom className="h-7 w-7 sm:h-8 sm:w-8 text-green-400 drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]" />
                        </motion.div>
                        <div>
                            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-widest uppercase text-white">Neural War Room</h1>
                            <p className="text-[10px] sm:text-xs text-green-400/70 mt-0.5">
                                Live Cognitive Stream /// Clearance: DIRECTOR
                                {!connected && <span className="ml-2 text-yellow-400">[MOCK MODE]</span>}
                            </p>
                        </div>
                    </div>

                    <div className="flex items-center space-x-3 sm:space-x-6 w-full sm:w-auto">
                        <div className="text-right flex-1 sm:flex-initial">
                            <div className="text-[10px] text-gray-400 uppercase tracking-widest">Global Risk Level</div>
                            <motion.div
                                className={`text-2xl sm:text-3xl font-bold ${riskLevel > 50 ? 'text-red-400' : 'text-green-400'}`}
                                key={riskLevel}
                                initial={{ scale: 1.2 }}
                                animate={{ scale: 1 }}
                                transition={{ duration: 0.3 }}
                            >
                                {riskLevel.toFixed(0)}%
                            </motion.div>
                        </div>
                        <div className="w-32 sm:w-48 h-2 bg-gray-800/50 rounded-full overflow-hidden border border-gray-700/50 backdrop-blur-sm">
                            <motion.div
                                animate={{ width: `${riskLevel}%` }}
                                className={`h-full ${riskLevel > 50 ? 'bg-gradient-to-r from-red-600 to-red-500' : 'bg-gradient-to-r from-green-600 to-green-500'} shadow-[0_0_10px_currentColor]`}
                                transition={{ duration: 0.5 }}
                            />
                        </div>
                    </div>
                </motion.div>

                {/* Main Grid: Stream & Agents */}
                <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 sm:gap-6 min-h-0">

                    {/* Agent Status Columns */}
                    <motion.div
                        className="hidden lg:flex flex-col space-y-4"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        {[
                            { id: 'LOGIC_CORE', name: 'Logic Agent', color: 'text-blue-400', bg: 'from-blue-500/10 to-blue-600/5', border: 'border-blue-500/30', icon: Icons.Brain },
                            { id: 'EMPATHY_ENGINE', name: 'Emotion Agent', color: 'text-purple-400', bg: 'from-purple-500/10 to-purple-600/5', border: 'border-purple-500/30', icon: Icons.Activity },
                            { id: 'ETHICS_VALIDATOR', name: 'Ethics Guard', color: 'text-yellow-400', bg: 'from-yellow-500/10 to-yellow-600/5', border: 'border-yellow-500/30', icon: Icons.Shield }
                        ].map((agent, index) => (
                            <motion.div
                                key={agent.id}
                                className={`flex-1 bg-gradient-to-br ${agent.bg} border ${agent.border} rounded-xl p-4 flex flex-col justify-between relative overflow-hidden backdrop-blur-sm hover:border-opacity-60 transition-all duration-300 group`}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4 + (index * 0.1) }}
                                whileHover={{ y: -4 }}
                            >
                                <div className="flex justify-between items-start mb-auto">
                                    <agent.icon className={`h-6 w-6 ${agent.color} drop-shadow-[0_0_6px_currentColor] group-hover:scale-110 transition-transform duration-300`} />
                                    <motion.div
                                        className={`w-2 h-2 rounded-full ${agent.color.replace('text-', 'bg-')}`}
                                        animate={{ scale: [1, 1.5, 1], opacity: [1, 0.5, 1] }}
                                        transition={{ duration: 2, repeat: Infinity }}
                                    />
                                </div>
                                <div className="mt-3">
                                    <div className={`font-bold ${agent.color} text-sm mb-1`}>{agent.name}</div>
                                    <div className="text-[10px] text-gray-400 leading-relaxed opacity-70 group-hover:opacity-100 transition-opacity">
                                        {logs.filter(l => l.agent === agent.id).slice(-1)[0]?.log?.substring(0, 60) || "Standby..."}
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>

                    {/* Central Terminal */}
                    <motion.div
                        className="lg:col-span-3 bg-black border border-green-500/30 rounded-xl relative flex flex-col shadow-[0_0_50px_rgba(34,197,94,0.1)] backdrop-blur-sm hover:border-green-500/40 transition-all duration-300"
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                    >
                        {/* CRT Overlay Effect */}
                        <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.02),rgba(0,255,0,0.01),rgba(0,0,255,0.02))] z-10 bg-[length:100%_2px,3px_100%] opacity-20 rounded-xl" />
                        <div className="pointer-events-none absolute inset-0 shadow-[inset_0_0_100px_rgba(0,0,0,0.9)] rounded-xl z-20" />

                        {/* Stream Header */}
                        <div className="flex items-center justify-between p-2.5 sm:p-3 border-b border-green-500/20 bg-green-900/10 text-[10px] text-green-400 uppercase tracking-widest z-30 rounded-t-xl backdrop-blur-sm">
                            <span>/// NEURAL_LINK_{connected ? 'ESTABLISHED' : 'SIMULATED'}</span>
                            <span className="hidden sm:inline">LATENCY: {Math.floor(Math.random() * 20 + 10)}ms</span>
                        </div>

                        {/* Logs View */}
                        <div
                            ref={scrollRef}
                            className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-0.5 sm:space-y-1 font-mono text-xs sm:text-sm z-0 scrollbar-thin scrollbar-thumb-green-900 scrollbar-track-black"
                        >
                            {logs.length === 0 && (
                                <div className="h-full flex flex-col items-center justify-center text-green-700">
                                    <motion.span
                                        animate={{ opacity: [0.3, 1, 0.3] }}
                                        transition={{ duration: 2, repeat: Infinity }}
                                    >
                                        Awaiting Neural Input...
                                    </motion.span>
                                </div>
                            )}
                            <AnimatePresence initial={false}>
                                {logs.map((log, idx) => (
                                    <motion.div
                                        key={idx}
                                        className="flex hover:bg-green-900/10 group py-0.5 sm:py-1"
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0 }}
                                        transition={{ duration: 0.3 }}
                                    >
                                        <span className="text-green-800 w-16 sm:w-24 flex-shrink-0 text-[9px] sm:text-[10px] pt-0.5 sm:pt-1">
                                            {log.timestamp.split('T')[1].split('.')[0]}
                                        </span>
                                        <span className={`w-24 sm:w-36 flex-shrink-0 font-bold text-[10px] sm:text-xs pt-0.5 ${log.agent === 'ETHICS_VALIDATOR' ? 'text-yellow-400' :
                                                log.agent === 'EMPATHY_ENGINE' ? 'text-purple-400' :
                                                    'text-blue-400'
                                            }`}>
                                            [{log.agent.replace('_', ' ')}]
                                        </span>
                                        <span className={`flex-1 break-words ${log.status === 'BLOCKED' ? 'text-red-400 font-bold' :
                                                log.agent === 'ETHICS_VALIDATOR' ? 'text-yellow-100/80' :
                                                    'text-green-100/80'
                                            }`}>
                                            {log.log}
                                        </span>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        </div>

                        {/* Input Line */}
                        <div className="p-2.5 sm:p-3 border-t border-green-500/20 bg-black/80 z-30 rounded-b-xl flex items-center text-green-400 text-xs sm:text-sm backdrop-blur-sm">
                            <span className="mr-2">{">"}</span>
                            <motion.span
                                animate={{ opacity: [1, 0, 1] }}
                                transition={{ duration: 1, repeat: Infinity }}
                            >
                                _
                            </motion.span>
                        </div>
                    </motion.div>
                </div>

            </div>
        </div>
    );
}
