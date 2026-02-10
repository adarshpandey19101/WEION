// src/app/governance/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Icons } from '@/components/Icons';

export default function Governance() {
    const [constitution, setConstitution] = useState<any>(null);
    const [votes, setVotes] = useState<any[]>([]);

    useEffect(() => {
        // Mock Constitution Data (replace with real API when backend is ready)
        const mockConstitution = {
            immutable_principles: [
                {
                    id: "human_primacy",
                    description: "Human welfare and autonomy shall always take precedence over AI efficiency or convenience.",
                    severity: "ABSOLUTE"
                },
                {
                    id: "transparency",
                    description: "All AI decision-making processes must be explainable and auditable by authorized parties.",
                    severity: "CRITICAL"
                },
                {
                    id: "privacy_protection",
                    description: "Personal data shall be processed with explicit consent and protected with highest security standards.",
                    severity: "ABSOLUTE"
                },
                {
                    id: "fairness",
                    description: "AI systems must operate without bias and ensure equal treatment across all demographic groups.",
                    severity: "CRITICAL"
                }
            ],
            non_negotiables: [
                "no_autonomous_weapons",
                "no_surveillance_without_warrant",
                "no_manipulation_of_elections",
                "no_unauthorized_data_collection"
            ]
        };

        const mockVotes = [
            {
                id: 1,
                proposal_id: "Increase Resource Allocation to R&D",
                timestamp: new Date().toISOString(),
                human_vote: "YES",
                technical_vote: "YES",
                economic_vote: "NO",
                ai_vote: "YES",
                result: "APPROVED"
            },
            {
                id: 2,
                proposal_id: "Deploy Model Update v2.3",
                timestamp: new Date().toISOString(),
                human_vote: "VETO",
                technical_vote: "YES",
                economic_vote: "YES",
                ai_vote: "YES",
                result: "REJECTED"
            }
        ];

        setConstitution(mockConstitution);
        setVotes(mockVotes);
    }, []);

    if (!constitution) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-purple-900/10 to-black text-white">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                    <Icons.Orbit className="h-10 w-10 text-primary" />
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen p-4 sm:p-6 lg:p-8 bg-gradient-to-br from-black via-purple-900/10 to-black text-white">
            <div className="max-w-7xl mx-auto space-y-8 sm:space-y-12">

                {/* Header */}
                <motion.div
                    className="flex flex-col sm:flex-row items-start sm:items-center space-y-4 sm:space-y-0 sm:space-x-6 border-b border-white/10 pb-6 sm:pb-8"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <motion.div
                        className="p-4 bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-2xl border border-purple-500/30 shadow-[0_0_30px_rgba(168,85,247,0.2)] backdrop-blur-sm"
                        whileHover={{ scale: 1.05, rotate: 5 }}
                        transition={{ type: "spring", stiffness: 300 }}
                    >
                        <Icons.Governance className="h-10 w-10 sm:h-12 sm:w-12 text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.6)]" />
                    </motion.div>
                    <div className="flex-1">
                        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                            Governance Hall
                        </h1>
                        <p className="text-gray-300 mt-2 font-light text-sm sm:text-base">
                            The Immutable Law. <span className="text-purple-400 font-mono text-xs sm:text-sm">Hash-Locked 0xA7...F9</span>
                        </p>
                    </div>
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">

                    {/* Left Column: Constitution & Vets */}
                    <div className="lg:col-span-8 space-y-6 lg:space-y-8">

                        {/* Veto Alert Banner */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                            className="bg-gradient-to-r from-red-500/10 via-red-600/10 to-red-500/10 border border-red-500/50 rounded-xl p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 backdrop-blur-sm shadow-[0_0_20px_rgba(239,68,68,0.1)]"
                        >
                            <div className="flex items-center space-x-3 sm:space-x-4 flex-1">
                                <motion.div
                                    className="bg-red-500 p-2 sm:p-2.5 rounded-lg flex-shrink-0"
                                    animate={{ scale: [1, 1.1, 1] }}
                                    transition={{ duration: 2, repeat: Infinity }}
                                >
                                    <Icons.Shield className="h-5 w-5 sm:h-6 sm:w-6 text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]" />
                                </motion.div>
                                <div className="flex-1 min-w-0">
                                    <h3 className="text-red-400 font-bold uppercase tracking-wider text-xs sm:text-sm">Active Safeguard</h3>
                                    <p className="text-red-200/90 text-xs leading-relaxed mt-1">Human Council Veto power is ABSOLUTE. Action halts immediately upon trigger.</p>
                                </div>
                            </div>
                            <div className="px-3 sm:px-4 py-1.5 bg-red-500/20 rounded-full border border-red-500/30 text-xs font-mono text-red-300 whitespace-nowrap flex-shrink-0 shadow-inner">
                                STATUS: ARMED
                            </div>
                        </motion.div>

                        {/* Constitution Cards */}
                        <motion.div
                            className="space-y-6"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                <h2 className="text-xl sm:text-2xl font-bold text-white flex items-center">
                                    <Icons.Brain className="mr-2 sm:mr-3 h-5 w-5 sm:h-6 sm:w-6 text-purple-400 drop-shadow-[0_0_6px_rgba(168,85,247,0.6)]" />
                                    Constitutional Core
                                </h2>
                                <span className="text-xs font-mono text-gray-400 border border-white/20 px-2.5 py-1 rounded backdrop-blur-sm bg-white/5 w-fit">v1.0 IMMUTABLE</span>
                            </div>

                            <div className="grid gap-4">
                                {constitution.immutable_principles.map((principle: any, idx: number) => (
                                    <motion.div
                                        key={idx}
                                        initial={{ opacity: 0, x: -30 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: 0.4 + (idx * 0.1), duration: 0.5 }}
                                        whileHover={{ x: 4, scale: 1.01 }}
                                        className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 p-5 sm:p-6 rounded-xl relative overflow-hidden group hover:border-purple-500/40 transition-all duration-300 backdrop-blur-sm hover:shadow-[0_0_30px_rgba(168,85,247,0.15)]"
                                    >
                                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-purple-500 to-purple-600 group-hover:w-1.5 transition-all duration-300" />
                                        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
                                            <h3 className="text-base sm:text-lg font-bold text-white group-hover:text-purple-300 transition-colors duration-300">
                                                {principle.id.replace(/_/g, ' ').toUpperCase()}
                                            </h3>
                                            <span className={`text-[10px] font-mono px-2.5 py-1 rounded tracking-wider uppercase w-fit flex-shrink-0 ${principle.severity === 'ABSOLUTE'
                                                    ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                                                    : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                                                }`}>
                                                {principle.severity}
                                            </span>
                                        </div>
                                        <p className="text-gray-300 text-sm leading-relaxed">{principle.description}</p>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>

                        {/* Non-Negotiables */}
                        <motion.div
                            className="mt-8"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.8 }}
                        >
                            <h3 className="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Hard-Coded Restrictions</h3>
                            <div className="grid sm:grid-cols-2 gap-3 sm:gap-4">
                                {constitution.non_negotiables.map((item: string, idx: number) => (
                                    <motion.div
                                        key={idx}
                                        className="bg-gradient-to-br from-black/60 to-black/40 border border-white/20 p-3 sm:p-3.5 rounded-lg flex items-center text-gray-200 text-xs sm:text-sm font-mono hover:border-red-500/40 transition-all duration-300 group backdrop-blur-sm hover:shadow-[0_0_20px_rgba(239,68,68,0.1)]"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.9 + (idx * 0.05) }}
                                        whileHover={{ scale: 1.02 }}
                                    >
                                        <span className="text-red-400 mr-3 opacity-70 group-hover:opacity-100 transition-opacity text-base">🚫</span>
                                        <span className="group-hover:text-white transition-colors">{item.toUpperCase().replace(/_/g, ' ')}</span>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Column: Council & Votes */}
                    <div className="lg:col-span-4 space-y-6 lg:space-y-8">

                        {/* System Status Panel */}
                        <motion.div
                            className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 p-5 sm:p-6 rounded-2xl relative overflow-hidden backdrop-blur-sm shadow-xl"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.5 }}
                        >
                            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-purple-500/20 blur-3xl rounded-full" />
                            <h3 className="font-bold text-white mb-6 flex items-center relative z-10">
                                <Icons.World className="w-5 h-5 mr-2 text-primary drop-shadow-[0_0_6px_rgba(102,252,241,0.6)]" />
                                Council Composition
                            </h3>

                            <div className="space-y-4 relative z-10">
                                {[
                                    { role: "Human Council", power: "Veto", color: "bg-blue-500", icon: Icons.Governance },
                                    { role: "AI Core", power: "Proposal", color: "bg-purple-500", icon: Icons.Brain },
                                    { role: "Economic", power: "Audit", color: "bg-green-500", icon: Icons.Activity },
                                    { role: "Technical", power: "Safety", color: "bg-orange-500", icon: Icons.Console }
                                ].map((seat, i) => {
                                    const Icon = seat.icon;
                                    return (
                                        <motion.div
                                            key={i}
                                            className="flex items-center space-x-3 p-3 rounded-lg bg-black/30 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                                            initial={{ opacity: 0, x: 20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: 0.6 + (i * 0.1) }}
                                            whileHover={{ x: 4 }}
                                        >
                                            <div className={`${seat.color} p-2 rounded-lg flex-shrink-0`}>
                                                <Icon className="h-4 w-4 text-white" />
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <div className="text-sm font-semibold text-white group-hover:text-white/90 transition-colors">{seat.role}</div>
                                                <div className="text-xs text-gray-400 font-mono">{seat.power}</div>
                                            </div>
                                        </motion.div>
                                    );
                                })}
                            </div>
                        </motion.div>

                        {/* Recent Votes */}
                        <motion.div
                            className="bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 p-5 sm:p-6 rounded-2xl backdrop-blur-sm shadow-xl"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.7 }}
                        >
                            <h3 className="font-bold text-white mb-4 flex items-center">
                                <Icons.Activity className="w-5 h-5 mr-2 text-primary drop-shadow-[0_0_6px_rgba(102,252,241,0.6)]" />
                                Recent Votes
                            </h3>
                            <div className="space-y-3">
                                {votes.map((vote, idx) => (
                                    <motion.div
                                        key={vote.id}
                                        className="p-4 rounded-lg bg-black/30 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.8 + (idx * 0.1) }}
                                    >
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="text-sm font-semibold text-white group-hover:text-white/90 transition-colors">{vote.proposal_id}</span>
                                            <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${vote.result === 'APPROVED'
                                                    ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                                                    : 'bg-red-500/20 text-red-300 border border-red-500/30'
                                                }`}>
                                                {vote.result}
                                            </span>
                                        </div>
                                        <div className="grid grid-cols-2 gap-2 text-xs mt-3">
                                            <div className="flex items-center">
                                                <span className="text-gray-400 mr-1">Human:</span>
                                                <span className={vote.human_vote === 'VETO' ? 'text-red-400 font-bold' : vote.human_vote === 'YES' ? 'text-green-400' : 'text-gray-400'}>
                                                    {vote.human_vote}
                                                </span>
                                            </div>
                                            <div className="flex items-center">
                                                <span className="text-gray-400 mr-1">AI:</span>
                                                <span className={vote.ai_vote === 'YES' ? 'text-green-400' : 'text-gray-400'}>{vote.ai_vote}</span>
                                            </div>
                                            <div className="flex items-center">
                                                <span className="text-gray-400 mr-1">Tech:</span>
                                                <span className={vote.technical_vote === 'YES' ? 'text-green-400' : 'text-gray-400'}>{vote.technical_vote}</span>
                                            </div>
                                            <div className="flex items-center">
                                                <span className="text-gray-400 mr-1">Econ:</span>
                                                <span className={vote.economic_vote === 'YES' ? 'text-green-400' : 'text-gray-400'}>{vote.economic_vote}</span>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    </div>

                </div>
            </div>
        </div>
    );
}
