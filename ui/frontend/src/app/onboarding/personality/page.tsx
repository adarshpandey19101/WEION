"use client";

import { Button } from "@/components/ui/button";
import { User, Cpu, Network, Zap } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { cn } from "@/lib/utils";

const personalities = [
    {
        id: "ceo",
        title: "The CEO",
        tagline: "Decisive, Strategic, High-Level",
        description: "Prioritizes big-picture goals and resource allocation. Communicates with brevity and focus on ROI.",
        icon: User,
        color: "text-red-400",
        bg: "bg-red-500/10",
        border: "hover:border-red-500/50"
    },
    {
        id: "cto",
        title: "The CTO",
        tagline: "Technical, Precise, Systemic",
        description: "Focuses on architecture, scalability, and technical correctness. Explores edge cases and failure modes.",
        icon: Cpu,
        color: "text-cyan-400",
        bg: "bg-cyan-500/10",
        border: "hover:border-cyan-500/50"
    },
    {
        id: "researcher",
        title: "The Researcher",
        tagline: "Curious, Thorough, Evidence-Based",
        description: "Digs deep into data, verifies sources, and synthesizes complex information. Values nuance over speed.",
        icon: Network,
        color: "text-purple-400",
        bg: "bg-purple-500/10",
        border: "hover:border-purple-500/50"
    },
    {
        id: "hacker",
        title: "The Hacker",
        tagline: "Creative, Unorthodox, fast",
        description: "Finds shortcuts and novel solutions. Willing to break rules to achieve the objective.",
        icon: Zap,
        color: "text-green-400",
        bg: "bg-green-500/10",
        border: "hover:border-green-500/50"
    }
];

export default function PersonalityPage() {
    const [selected, setSelected] = useState<string | null>(null);

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4">
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />

            <div className="relative z-10 w-full max-w-5xl">
                <div className="text-center mb-10">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
                        Select your Co-pilot
                    </h1>
                    <p className="text-slate-400">
                        Who do you want by your side?
                    </p>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {personalities.map((p) => (
                        <button
                            key={p.id}
                            onClick={() => setSelected(p.id)}
                            className={cn(
                                "group relative flex flex-col items-start p-6 rounded-xl border bg-slate-900/50 transition-all text-left",
                                selected === p.id
                                    ? "border-cyan-500 ring-1 ring-cyan-500/50 bg-slate-900/80"
                                    : "border-slate-800 hover:bg-slate-800/50",
                                p.border
                            )}
                        >
                            <div className={cn("w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-colors", p.bg, p.color)}>
                                <p.icon className="w-6 h-6" />
                            </div>
                            <h3 className="text-lg font-bold text-white">{p.title}</h3>
                            <div className="text-xs font-medium text-cyan-400 mb-2 uppercase tracking-wider">{p.tagline}</div>
                            <p className="text-sm text-slate-400">{p.description}</p>

                            {selected === p.id && (
                                <div className="absolute top-4 right-4 w-3 h-3 rounded-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]" />
                            )}
                        </button>
                    ))}
                </div>

                <div className="mt-10 flex justify-between max-w-2xl mx-auto">
                    <Button variant="ghost" asChild>
                        <Link href="/onboarding/preferences">Back</Link>
                    </Button>
                    <Button className="bg-cyan-600 hover:bg-cyan-700 text-white px-8" asChild>
                        <Link href="/dashboard">Initialize System</Link>
                    </Button>
                </div>
            </div>
        </div>
    );
}
