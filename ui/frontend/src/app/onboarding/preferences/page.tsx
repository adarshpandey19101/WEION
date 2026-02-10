"use client";

import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import Link from "next/link";
import { useState } from "react";

export default function PreferencesPage() {
    const [speedVsQuality, setSpeedVsQuality] = useState([50]);
    const [riskTolerance, setRiskTolerance] = useState([30]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4">
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />

            <div className="relative z-10 w-full max-w-2xl">
                <div className="text-center mb-10">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
                        Calibrate your System
                    </h1>
                    <p className="text-slate-400">
                        Define how WEION should trade off conflicting objectives.
                    </p>
                </div>

                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 space-y-10 backdrop-blur-sm">

                    {/* Speed vs Quality */}
                    <div className="space-y-4">
                        <div className="flex justify-between items-center text-sm font-medium">
                            <span className="text-cyan-400">Maximize Speed</span>
                            <span className="text-slate-400">Balance</span>
                            <span className="text-purple-400">Maximize Quality</span>
                        </div>
                        <Slider
                            value={speedVsQuality}
                            onValueChange={setSpeedVsQuality}
                            max={100}
                            step={1}
                            className="py-4"
                        />
                        <div className="p-4 rounded-lg bg-slate-800/50 text-sm text-slate-400 border border-slate-700/50">
                            {speedVsQuality[0] < 30 && "I will execute tasks rapidly, accepting minor errors for speed."}
                            {speedVsQuality[0] >= 30 && speedVsQuality[0] <= 70 && "I will balance execution speed with thorough verification."}
                            {speedVsQuality[0] > 70 && "I will double-check every step, prioritizing precision over speed."}
                        </div>
                    </div>

                    {/* Risk Tolerance */}
                    <div className="space-y-4">
                        <div className="flex justify-between items-center text-sm font-medium">
                            <span className="text-green-400">Conservative</span>
                            <span className="text-slate-400">Moderate</span>
                            <span className="text-red-400">Experimental</span>
                        </div>
                        <Slider
                            value={riskTolerance}
                            onValueChange={setRiskTolerance}
                            max={100}
                            step={1}
                            className="py-4"
                        />
                        <div className="p-4 rounded-lg bg-slate-800/50 text-sm text-slate-400 border border-slate-700/50">
                            {riskTolerance[0] < 30 && "I will only take actions with high certainty and low downside risks."}
                            {riskTolerance[0] >= 30 && riskTolerance[0] <= 70 && "I will take calculated risks when the expected value is positive."}
                            {riskTolerance[0] > 70 && "I will attempt novel strategies and explore uncertain paths to find breakthroughs."}
                        </div>
                    </div>

                </div>

                <div className="mt-10 flex justify-between">
                    <Button variant="ghost" asChild>
                        <Link href="/role-selection">Back</Link>
                    </Button>
                    <Button className="bg-cyan-600 hover:bg-cyan-700 text-white" asChild>
                        <Link href="/onboarding/personality">Continue</Link>
                    </Button>
                </div>
            </div>
        </div>
    );
}
