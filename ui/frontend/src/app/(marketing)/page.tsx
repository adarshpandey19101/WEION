"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, Zap, Shield, Database } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Section */}
            <section className="pt-32 pb-16 md:pt-48 md:pb-32 px-6 text-center">
                <div className="max-w-4xl mx-auto space-y-8 fade-in">
                    <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                        <span className="flex h-2 w-2 rounded-full bg-blue-500 mr-2 animate-pulse"></span>
                        WEION Enterprise 1.0 is plain-text auditable.
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground">
                        The Cognitive Operating System for the Modern Enterprise.
                    </h1>

                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                        Autonomous agents that plan, reason, and execute complex workflows.
                        Built with a constitution-first architecture for total trust.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                        <Button size="lg" className="h-12 px-8 text-base rounded-full" asChild>
                            <Link href="/signup">
                                Start Building <ArrowRight className="ml-2 w-4 h-4" />
                            </Link>
                        </Button>
                        <Button variant="outline" size="lg" className="h-12 px-8 text-base rounded-full" asChild>
                            <Link href="/contact">Book a Demo</Link>
                        </Button>
                    </div>
                </div>
            </section>

            {/* Features Grid */}
            <section className="py-24 bg-zinc-950/50 border-y border-border/50">
                <div className="container mx-auto px-6">
                    <div className="grid md:grid-cols-3 gap-12">
                        <div className="space-y-4">
                            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20">
                                <Zap className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-xl font-semibold">Autonomous Execution</h3>
                            <p className="text-muted-foreground leading-relaxed">
                                WEION doesn't just chat. It uses tools, browses the web, and integrates with your APIs to complete end-to-end tasks.
                            </p>
                        </div>
                        <div className="space-y-4">
                            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20">
                                <Shield className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-xl font-semibold">Governance & Trust</h3>
                            <p className="text-muted-foreground leading-relaxed">
                                Define a constitution for your agents. Every action is logged, auditable, and subject to human veto.
                            </p>
                        </div>
                        <div className="space-y-4">
                            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20">
                                <Database className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-xl font-semibold">Enterprise Memory</h3>
                            <p className="text-muted-foreground leading-relaxed">
                                A shared knowledge graph that grows with your organization. Agents learn from past missions and avoid repeating mistakes.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Social Proof / Trusted By */}
            <section className="py-20 border-b border-border/50">
                <div className="container mx-auto px-6 text-center">
                    <p className="text-sm font-medium text-muted-foreground mb-8">TRUSTED BY TEAMS AT</p>
                    <div className="flex flex-wrap justify-center gap-12 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
                        {/* Placeholders for logos */}
                        <div className="text-xl font-bold">ACME Corp</div>
                        <div className="text-xl font-bold">Globex</div>
                        <div className="text-xl font-bold">Soylent</div>
                        <div className="text-xl font-bold">Initech</div>
                        <div className="text-xl font-bold">Umbrella</div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-32 text-center">
                <div className="container mx-auto px-6 max-w-3xl space-y-8">
                    <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Ready to scale your workforce?</h2>
                    <p className="text-lg text-muted-foreground">
                        Deploy your first autonomous agent in minutes. No credit card required for the pilot tier.
                    </p>
                    <Button size="lg" className="h-12 px-8 rounded-full" asChild>
                        <Link href="/signup">Get Started Now</Link>
                    </Button>
                    <div className="flex justify-center gap-6 text-sm text-muted-foreground pt-4">
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" /> SOC2 Certified
                        </div>
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" /> GDPR Compliant
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
