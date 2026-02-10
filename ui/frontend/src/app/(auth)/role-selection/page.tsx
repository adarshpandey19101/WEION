"use client";

import { Button } from "@/components/ui/button";
import { GraduationCap, Briefcase, Building2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { cn } from "@/lib/utils";

const roles = [
    {
        id: "student",
        title: "Student / Researcher",
        description: "I want to augment my learning and research capabilities.",
        icon: GraduationCap,
        color: "text-cyan-400",
        bg: "bg-cyan-500/10",
        border: "hover:border-cyan-500/50"
    },
    {
        id: "professional",
        title: "Professional",
        description: "I need an autonomous executive assistant to optimize my work.",
        icon: Briefcase,
        color: "text-purple-400",
        bg: "bg-purple-500/10",
        border: "hover:border-purple-500/50"
    },
    {
        id: "org",
        title: "Organization User",
        description: "I am part of a team deploying WEION for enterprise ops.",
        icon: Building2,
        color: "text-blue-400",
        bg: "bg-blue-500/10",
        border: "hover:border-blue-500/50"
    }
];

export default function RoleSelectionPage() {
    const [selectedRole, setSelectedRole] = useState<string | null>(null);

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4">
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />

            <div className="relative z-10 w-full max-w-4xl">
                <div className="text-center mb-10">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
                        Choose your archetype
                    </h1>
                    <p className="text-slate-400">
                        WEION adapts its cognitive architecture based on your role.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                    {roles.map((role) => (
                        <button
                            key={role.id}
                            onClick={() => setSelectedRole(role.id)}
                            className={cn(
                                "group relative flex flex-col items-start p-6 rounded-xl border bg-slate-900/50 transition-all text-left",
                                selectedRole === role.id
                                    ? "border-cyan-500 ring-1 ring-cyan-500/50 bg-slate-900/80"
                                    : "border-slate-800 hover:bg-slate-800/50",
                                role.border
                            )}
                        >
                            <div className={cn("w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-colors", role.bg, role.color)}>
                                <role.icon className="w-6 h-6" />
                            </div>
                            <h3 className="text-lg font-bold text-white mb-2">{role.title}</h3>
                            <p className="text-sm text-slate-400">{role.description}</p>

                            {selectedRole === role.id && (
                                <div className="absolute top-4 right-4 w-3 h-3 rounded-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]" />
                            )}
                        </button>
                    ))}
                </div>

                <div className="mt-10 flex justify-center">
                    <Button
                        size="lg"
                        className="w-full md:w-auto min-w-[200px] bg-cyan-600 hover:bg-cyan-700"
                        disabled={!selectedRole}
                        asChild={!!selectedRole}
                    >
                        {selectedRole ? <Link href="/onboarding/preferences">Continue</Link> : "Select a Role"}
                    </Button>
                </div>
            </div>
        </div>
    );
}
