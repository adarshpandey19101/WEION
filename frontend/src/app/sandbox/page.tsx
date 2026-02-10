
// src/app/sandbox/page.tsx
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Icons } from '@/components/Icons';

export default function Sandbox() {
    const [decision, setDecision] = useState("Implement Universal Basic Compute");
    const [duration, setDuration] = useState(50); // Steps
    const [horizon, setHorizon] = useState("1k"); // 100y, 1k, 10k
    const [autonomy, setAutonomy] = useState(50);
    const [risk, setRisk] = useState(20);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const runSimulation = async () => {
        setLoading(true);
        setResult(null);

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Generate mock simulation results based on parameters
        const generateMockTimeline = () => {
            const timeline = [];
            const years = horizon === '100y' ? 100 : horizon === '1k' ? 1000 : 10000;
            const steps = Math.min(duration, 100);

            for (let i = 0; i <= steps; i++) {
                const year = Math.floor((i / steps) * years);
                const progress = i / steps;

                // Social trust decreases with high autonomy
                const trustBase = 0.7 - (autonomy / 200);
                const trust = Math.max(0, Math.min(1, trustBase - progress * (risk / 100) * 0.3));

                // Inequality increases with low autonomy oversight
                const inequalityBase = 0.3 + (autonomy / 150);
                const inequality = Math.max(0, Math.min(1, inequalityBase + progress * (risk / 200)));

                // Economy fluctuates based on risk
                const economyBase = 0.6;
                const economy = Math.max(0, Math.min(1, economyBase + Math.sin(progress * Math.PI * 2) * (risk / 100) * 0.3));

                timeline.push({
                    year: year,
                    world_state: {
                        social_trust: parseFloat(trust.toFixed(3)),
                        inequality: parseFloat(inequality.toFixed(3)),
                        economy: parseFloat(economy.toFixed(3))
                    }
                });
            }
            return timeline;
        };

        const timeline = generateMockTimeline();
        const finalState = timeline[timeline.length - 1].world_state;

        // Determine risks and status
        const risks = [];
        if (finalState.social_trust < 0.3) risks.push("Critical erosion of social trust detected");
        if (finalState.inequality > 0.7) risks.push("Severe wealth concentration threatening stability");
        if (autonomy > 80 && risk > 60) risks.push("High autonomy + high risk = potential loss of control");

        const isSafe = risks.length === 0 && finalState.social_trust > 0.4;

        // Generate narrative
        const narrative = `SIMULATION INITIALIZED: ${decision}
Horizon: ${horizon} | Autonomy: ${autonomy}% | Risk: ${risk}%

Year 0: Policy implementation begins
${autonomy > 60 ? '⚠️ High autonomy detected - oversight mechanisms activated' : ''}
${risk > 50 ? '⚠️ Elevated risk tolerance - monitoring critical thresholds' : ''}

Year ${Math.floor(timeline.length / 3)}: Early indicators
- Social trust ${finalState.social_trust > 0.5 ? 'stabilizing' : '🔴 declining'}
- Economic power ${finalState.economy > 0.5 ? 'growing' : 'volatile'}

Year ${Math.floor(timeline.length * 2 / 3)}: Mid-term assessment
- Inequality ${finalState.inequality < 0.5 ? 'controlled' : '🔴 rising dangerously'}

Year ${timeline[timeline.length - 1].year}: Final state reached
${isSafe ? '✓ Simulation completed within safe parameters' : '🔴 CRITICAL: Unacceptable outcome detected'}`;

        const mockResult = {
            timeline: timeline,
            final_status: isSafe ? 'SAFE' : 'AT_RISK',
            risks_detected: risks,
            narrative: narrative
        };

        setResult(mockResult);
        setLoading(false);

        // TODO: Replace with real API call when backend is available
        // try {
        //     const res = await fetch('http://localhost:8000/api/simulation/run', {
        //         method: 'POST',
        //         headers: { 'Content-Type': 'application/json' },
        //         body: JSON.stringify({ decision, duration_steps: duration, autonomy, risk, horizon })
        //     });
        //     const data = await res.json();
        //     setResult(data);
        // } catch (error) {
        //     console.error("Simulation failed:", error);
        // }
    };

    return (
        <div className="min-h-screen p-4 sm:p-6 lg:p-8 bg-gradient-to-br from-black via-cyan-900/5 to-black text-white">
            <div className="max-w-7xl mx-auto space-y-6 sm:space-y-8">

                {/* Header */}
                <motion.div
                    className="flex flex-col sm:flex-row items-start sm:items-center space-y-4 sm:space-y-0 sm:space-x-6 border-b border-white/10 pb-6 sm:pb-8"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <motion.div
                        className="p-3 sm:p-4 bg-gradient-to-br from-primary/20 to-cyan-600/10 rounded-2xl border border-primary/30 shadow-[0_0_30px_rgba(102,252,241,0.15)] backdrop-blur-sm"
                        whileHover={{ scale: 1.05, rotate: 5 }}
                        transition={{ type: "spring", stiffness: 300 }}
                    >
                        <Icons.Time className="h-9 w-9 sm:h-10 sm:w-10 text-primary drop-shadow-[0_0_8px_rgba(102,252,241,0.8)]" />
                    </motion.div>
                    <div className="flex-1">
                        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-400">Civilization Time Machine</h1>
                        <p className="text-gray-300 mt-2 font-light text-sm sm:text-base">Simulate future consequences before reality exists. <span className="text-primary font-mono text-xs">v1.0.4</span></p>
                    </div>
                </motion.div>

                {/* Control Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

                    {/* Input Console */}
                    <div className="lg:col-span-4 space-y-6">
                        <div className="bg-surface p-6 rounded-2xl border border-white/5 shadow-lg backdrop-blur-sm">
                            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center">
                                <Icons.Console className="w-4 h-4 mr-2" /> Simulation Parameters
                            </h3>

                            {/* Decision Input */}
                            <div className="mb-6">
                                <label className="block text-xs font-mono text-gray-400 mb-2">POLICY DIRECTIVE</label>
                                <textarea
                                    value={decision}
                                    onChange={(e) => setDecision(e.target.value)}
                                    className="w-full bg-black/40 border border-white/10 rounded-lg p-3 text-white text-sm focus:border-primary/50 focus:ring-1 focus:ring-primary/50 h-32 resize-none font-mono"
                                />
                            </div>

                            {/* Sliders */}
                            <div className="space-y-6 mb-8">
                                <div>
                                    <div className="flex justify-between text-xs mb-2 text-gray-400">
                                        <span>AUTONOMY LEVEL</span>
                                        <span className="text-primary">{autonomy}%</span>
                                    </div>
                                    <input
                                        type="range" min="0" max="100" value={autonomy} onChange={(e) => setAutonomy(parseInt(e.target.value))}
                                        className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary"
                                    />
                                </div>
                                <div>
                                    <div className="flex justify-between text-xs mb-2 text-gray-400">
                                        <span>RISK TOLERANCE</span>
                                        <span className="text-red-400">{risk}%</span>
                                    </div>
                                    <input
                                        type="range" min="0" max="100" value={risk} onChange={(e) => setRisk(parseInt(e.target.value))}
                                        className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-500"
                                    />
                                </div>
                            </div>

                            {/* Horizon Selector */}
                            <div className="grid grid-cols-3 gap-2 mb-8">
                                {['100y', '1k', '10k'].map((h) => (
                                    <button
                                        key={h}
                                        onClick={() => setHorizon(h)}
                                        className={`py-2 text-xs font-bold rounded-lg border transition-all ${horizon === h
                                            ? 'bg-primary/20 border-primary text-primary'
                                            : 'bg-black/20 border-white/10 text-gray-500 hover:text-white'
                                            }`}
                                    >
                                        {h.toUpperCase()}
                                    </button>
                                ))}
                            </div>

                            <button
                                onClick={runSimulation}
                                disabled={loading}
                                className="w-full py-4 bg-gradient-to-r from-primary to-blue-500 text-black font-bold rounded-xl hover:shadow-[0_0_20px_rgba(102,252,241,0.3)] transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]"
                            >
                                {loading ? (
                                    <Icons.Orbit className="animate-spin h-5 w-5" />
                                ) : (
                                    <>
                                        <Icons.Power className="h-5 w-5" />
                                        <span>INITIATE SIMULATION</span>
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Visualization Console */}
                    <div className="lg:col-span-8 space-y-6">
                        {result ? (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.98 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="space-y-6"
                            >
                                {/* Graph */}
                                <div className="bg-surface p-6 rounded-2xl border border-white/5 shadow-2xl relative overflow-hidden h-[400px]">
                                    <div className="absolute top-0 right-0 p-4 opacity-50">
                                        <span className="text-xs font-mono text-gray-500">REAL-TIME PROJECTION</span>
                                    </div>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={result.timeline}>
                                            <defs>
                                                <linearGradient id="colorTrust" x1="0" y1="0" x2="0" y2="1">
                                                    <stop offset="5%" stopColor="#66FCF1" stopOpacity={0.8} />
                                                    <stop offset="95%" stopColor="#66FCF1" stopOpacity={0} />
                                                </linearGradient>
                                            </defs>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                                            <XAxis dataKey="year" stroke="#444" tick={{ fontSize: 10 }} />
                                            <YAxis domain={[0, 1]} stroke="#444" tick={{ fontSize: 10 }} />
                                            <Tooltip
                                                contentStyle={{ backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px' }}
                                                itemStyle={{ fontSize: '12px' }}
                                            />
                                            <Legend />
                                            <Line type="monotone" dataKey="world_state.social_trust" name="Trust" stroke="#66FCF1" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
                                            <Line type="monotone" dataKey="world_state.inequality" name="Inequality" stroke="#F87171" strokeWidth={2} dot={false} />
                                            <Line type="monotone" dataKey="world_state.economy" name="Power" stroke="#A78BFA" strokeWidth={2} dot={false} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>

                                {/* Bottom Panels */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {/* Status */}
                                    <div className="bg-surface p-6 rounded-2xl border border-white/5 relative overflow-hidden">
                                        <div className={`absolute left-0 top-0 bottom-0 w-1 ${result.final_status === 'SAFE' ? 'bg-green-500' : 'bg-red-500'}`} />
                                        <h4 className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-2">OUTCOME ANALYSIS</h4>
                                        <div className={`text-3xl font-bold mb-4 ${result.final_status === 'SAFE' ? 'text-green-400' : 'text-red-500'}`}>
                                            {result.final_status}
                                        </div>
                                        {result.risks_detected.length > 0 ? (
                                            <div className="space-y-2">
                                                {result.risks_detected.map((risk: string, i: number) => (
                                                    <div key={i} className="flex items-start text-red-300 text-xs bg-red-900/10 p-2 rounded">
                                                        <Icons.Alert className="w-3 h-3 mr-2 mt-0.5 flex-shrink-0" />
                                                        <span>{risk}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        ) : (
                                            <span className="text-green-500/50 text-xs">No existential risks detected.</span>
                                        )}
                                    </div>

                                    {/* Narrative */}
                                    <div className="bg-surface p-6 rounded-2xl border border-white/5 flex flex-col h-64">
                                        <h4 className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-4 flex justify-between">
                                            <span>NARRATIVE LOG</span>
                                            <span className="text-primary animate-pulse">● LIVE</span>
                                        </h4>
                                        <div className="overflow-y-auto pr-2 space-y-3 font-mono text-xs leading-relaxed text-gray-300 scrollbar-thin">
                                            {result.narrative.split('\n').map((line: string, i: number) => {
                                                if (line.includes('⚠️')) return <p key={i} className="text-yellow-400 border-l-2 border-yellow-500 pl-2">{line}</p>;
                                                if (line.includes('🔴')) return <p key={i} className="text-primary border-l-2 border-primary pl-2">{line}</p>;
                                                return <p key={i} className="opacity-80">{line}</p>;
                                            })}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ) : (
                            <div className="h-full min-h-[400px] flex flex-col items-center justify-center border border-white/5 border-dashed rounded-2xl bg-white/5">
                                <Icons.Brain className="h-16 w-16 mb-4 text-gray-600 opacity-50" />
                                <p className="text-gray-500">Awaiting Simulation Parameters...</p>
                            </div>
                        )}
                    </div>

                </div>
            </div>
        </div>
    );
}
