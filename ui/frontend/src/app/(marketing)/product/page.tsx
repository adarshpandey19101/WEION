"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, Brain, Layers, Zap, Terminal, GitBranch } from "lucide-react";
import Link from "next/link";

export default function ProductPage() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero */}
            <section className="py-24 px-6 text-center bg-background">
                <div className="max-w-4xl mx-auto space-y-6">
                    <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium text-muted-foreground">
                        <Terminal className="w-3 h-3 mr-2" />
                        v1.0 Architecture Overview
                    </div>
                    <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
                        Reasoning first.<br />Action second.
                    </h1>
                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                        A look inside the WEION Cognitive Engine. How we moved beyond simple chatbots to autonomous agents.
                    </p>
                </div>
            </section>

            {/* Architecture Steps */}
            <section className="py-20 px-6">
                <div className="container mx-auto max-w-5xl space-y-24">
                    {/* Step 1 */}
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div className="order-2 md:order-1 space-y-6">
                            <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center border border-blue-500/20">
                                <Brain className="w-6 h-6 text-blue-500" />
                            </div>
                            <h2 className="text-3xl font-bold tracking-tight">Phase 1: Perception & Context</h2>
                            <p className="text-lg text-muted-foreground leading-relaxed">
                                Before acting, WEION builds a complete world model. It ingests documents, reads emails, and queries your databases to understand the full context of the mission.
                            </p>
                            <ul className="space-y-3 text-sm font-medium">
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-3" /> Multi-modal ingestion (PDF, CSV, Images)</li>
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-3" /> Real-time web browsing</li>
                            </ul>
                        </div>
                        <div className="order-1 md:order-2 bg-secondary/50 rounded-2xl p-8 aspect-square flex items-center justify-center border border-border/50">
                            <div className="text-muted-foreground font-mono text-xs">
                                [System Diagram: Input Processing]
                            </div>
                        </div>
                    </div>

                    {/* Step 2 */}
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div className="bg-secondary/50 rounded-2xl p-8 aspect-square flex items-center justify-center border border-border/50">
                            <div className="text-muted-foreground font-mono text-xs">
                                [System Diagram: Planning Tree]
                            </div>
                        </div>
                        <div className="space-y-6">
                            <div className="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center border border-purple-500/20">
                                <GitBranch className="w-6 h-6 text-purple-500" />
                            </div>
                            <h2 className="text-3xl font-bold tracking-tight">Phase 2: Reasoning & Planning</h2>
                            <p className="text-lg text-muted-foreground leading-relaxed">
                                WEION doesn't guess. It uses Chain-of-Thought reasoning to break complex goals into manageable steps. It simulates potential outcomes before executing a single command.
                            </p>
                            <ul className="space-y-3 text-sm font-medium">
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-purple-500 mr-3" /> Recursive task decomposition</li>
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-purple-500 mr-3" /> Self-correction loops</li>
                            </ul>
                        </div>
                    </div>

                    {/* Step 3 */}
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div className="order-2 md:order-1 space-y-6">
                            <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center border border-green-500/20">
                                <Zap className="w-6 h-6 text-green-500" />
                            </div>
                            <h2 className="text-3xl font-bold tracking-tight">Phase 3: Execution & Learning</h2>
                            <p className="text-lg text-muted-foreground leading-relaxed">
                                The agent uses tool-use capabilities to interact with the real world. Every success and failure is recorded in the Enterprise Memory, making the system smarter over time.
                            </p>
                            <ul className="space-y-3 text-sm font-medium">
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-green-500 mr-3" /> Secure API integrations</li>
                                <li className="flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-green-500 mr-3" /> Persistent long-term memory</li>
                            </ul>
                        </div>
                        <div className="order-1 md:order-2 bg-secondary/50 rounded-2xl p-8 aspect-square flex items-center justify-center border border-border/50">
                            <div className="text-muted-foreground font-mono text-xs">
                                [System Diagram: Tool Execution]
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
