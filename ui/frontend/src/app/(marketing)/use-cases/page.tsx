"use client";

import { Briefcase, GraduationCap, Building2, Gavel, ArrowRight, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const cases = [
    {
        icon: GraduationCap,
        title: "Research & Academia",
        description: "Accelerate literature review and hypothesis generation. Have WEION read thousands of papers and synthesize findings.",
        color: "text-blue-500",
        bg: "bg-blue-500/10",
        points: ["Automated Literature Review", "Data Synthesis", "Citation Management"]
    },
    {
        icon: Briefcase,
        title: "Startups & Founders",
        description: "Your first 10 hires in one system. Execute marketing, sales outreach, and basic operational workflows autonomously.",
        color: "text-purple-500",
        bg: "bg-purple-500/10",
        points: ["Autonomous SDR", "Content Generation", "Competitor Tracking"]
    },
    {
        icon: Building2,
        title: "Enterprise Operations",
        description: "Streamline complex supply chain, HR, and finance workflows with full audit trails and human-in-the-loop governance.",
        color: "text-orange-500",
        bg: "bg-orange-500/10",
        points: ["Supply Chain Optimization", "Automated Compliance", "Financial Forecasting"]
    },
    {
        icon: Gavel,
        title: "Public Sector",
        description: "Deploy secure, compliant AI for citizen services. Built with strict data sovereignty and constitutional guardrails.",
        color: "text-green-500",
        bg: "bg-green-500/10",
        points: ["Citizen Query Handling", "Policy Analysis", "Secure Document Processing"]
    }
];

export default function UseCasesPage() {
    return (
        <div className="flex flex-col min-h-screen">
            <section className="py-24 px-6 bg-background">
                <div className="container mx-auto max-w-5xl">
                    <div className="text-center mb-20 space-y-4">
                        <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Built for every scale.</h1>
                        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                            From solo researchers to sovereign governments, WEION scales its cognitive architecture to meet your needs.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8">
                        {cases.map((useCase, idx) => (
                            <div key={idx} className="group p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-all duration-300">
                                <div className={`w-12 h-12 rounded-lg ${useCase.bg} flex items-center justify-center mb-6`}>
                                    <useCase.icon className={`w-6 h-6 ${useCase.color}`} />
                                </div>
                                <h3 className="text-2xl font-semibold mb-3">{useCase.title}</h3>
                                <p className="text-muted-foreground mb-6 leading-relaxed">
                                    {useCase.description}
                                </p>
                                <ul className="space-y-3 mb-8">
                                    {useCase.points.map((point) => (
                                        <li key={point} className="flex items-center text-sm text-foreground/80">
                                            <Check className="w-4 h-4 mr-2 text-primary" />
                                            {point}
                                        </li>
                                    ))}
                                </ul>
                                <Button variant="outline" className="w-full group-hover:bg-secondary">
                                    Learn more <ArrowRight className="w-4 h-4 ml-2 opacity-50 group-hover:translate-x-1 transition-all" />
                                </Button>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <section className="py-24 border-t bg-secondary/30">
                <div className="container mx-auto px-6 text-center max-w-3xl space-y-8">
                    <h2 className="text-3xl font-bold tracking-tight">Ready to transform your workflow?</h2>
                    <Button size="lg" className="rounded-full px-8 h-12" asChild>
                        <Link href="/contact">Talk to Sales</Link>
                    </Button>
                </div>
            </section>
        </div>
    );
}
