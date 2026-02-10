"use client";

import { FileText, Lock, Eye, Scale } from "lucide-react";

export default function TrustPage() {
    return (
        <div className="flex flex-col min-h-screen">
            <section className="py-24 px-6 bg-background border-b">
                <div className="container mx-auto max-w-4xl text-center space-y-6">
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Trust is the API.</h1>
                    <p className="text-xl text-muted-foreground leading-relaxed">
                        We don't just ask you to trust the AI. We give you the tools to verify, audit, and veto its actions.
                    </p>
                </div>
            </section>

            <section className="py-24 px-6">
                <div className="container mx-auto max-w-4xl space-y-16">
                    {/* Section 1 */}
                    <div className="flex gap-6 md:gap-10">
                        <div className="shrink-0 pt-1">
                            <div className="w-12 h-12 rounded-full bg-secondary flex items-center justify-center border">
                                <FileText className="w-5 h-5" />
                            </div>
                        </div>
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold">Constitutional AI</h2>
                            <p className="text-muted-foreground leading-relaxed">
                                Every WEION agent operates under a rigid constitution. This isn't just a prompt—it's a system-level constraint layer that evaluates every planned action before execution. If an action violates a core tenet (e.g., "Do not exfiltrate PII"), the reasoning engine halts and flags the incident for human review.
                            </p>
                        </div>
                    </div>

                    {/* Section 2 */}
                    <div className="flex gap-6 md:gap-10">
                        <div className="shrink-0 pt-1">
                            <div className="w-12 h-12 rounded-full bg-secondary flex items-center justify-center border">
                                <Lock className="w-5 h-5" />
                            </div>
                        </div>
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold">Human Veto Power</h2>
                            <p className="text-muted-foreground leading-relaxed">
                                Autonomy doesn't mean lack of control. You define the "blast radius" for every agent. Low-risk actions (drafting emails) can be fully autonomous. High-risk actions (deploying code, transferring funds) require explicit "human-in-the-loop" approval via Slack, Email, or the WEION Console.
                            </p>
                        </div>
                    </div>

                    {/* Section 3 */}
                    <div className="flex gap-6 md:gap-10">
                        <div className="shrink-0 pt-1">
                            <div className="w-12 h-12 rounded-full bg-secondary flex items-center justify-center border">
                                <Eye className="w-5 h-5" />
                            </div>
                        </div>
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold">Total Auditability</h2>
                            <p className="text-muted-foreground leading-relaxed">
                                Black boxes are unacceptable in the enterprise. WEION logs the full "Chain of Thought" for every decision. You can inspect the exact reasoning steps, the documents retrieved, and the tool outputs that led to a specific outcome. This immutable log is your source of truth for compliance and debugging.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
