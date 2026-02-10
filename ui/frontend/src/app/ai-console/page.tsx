"use client";

import { DashboardShell } from "@/components/layout/DashboardShell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Send, Paperclip, Mic, Play } from "lucide-react";

export default function AIConsolePage() {
    return (
        <DashboardShell>
            <div className="flex flex-col h-[calc(100vh-8rem)]">
                <div className="flex items-center justify-between mb-4">
                    <h1 className="text-2xl font-bold text-white">Mission Control</h1>
                    <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="border-slate-700">
                            <Play className="w-4 h-4 mr-2 text-green-400" />
                            New Mission
                        </Button>
                    </div>
                </div>

                <Card className="flex-1 flex flex-col border-slate-800 bg-slate-900/50 overflow-hidden">
                    {/* Chat Area */}
                    <div className="flex-1 p-6 overflow-y-auto space-y-6">
                        {/* System Welcome */}
                        <div className="flex gap-4 max-w-3xl mx-auto">
                            <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center shrink-0">
                                <div className="w-4 h-4 bg-cyan-500 rounded-full" />
                            </div>
                            <div className="space-y-1">
                                <div className="text-sm font-bold text-cyan-400">WEION Core</div>
                                <div className="text-slate-300 text-sm leading-relaxed">
                                    Systems online. All cognitive modules are active. I am ready to plan and execute complex missions. What is our objective today?
                                </div>
                            </div>
                        </div>

                        {/* User Message */}
                        <div className="flex gap-4 max-w-3xl mx-auto flex-row-reverse">
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                                <div className="text-xs font-bold text-white">AK</div>
                            </div>
                            <div className="space-y-1 text-right">
                                <div className="text-sm font-bold text-slate-400">You</div>
                                <div className="bg-slate-800 text-slate-200 text-sm p-3 rounded-2xl rounded-tr-sm inline-block text-left">
                                    Analyze the competitor report I just uploaded and draft a counter-strategy for Q3.
                                </div>
                            </div>
                        </div>

                        {/* Execution Trace (Simulated) */}
                        <div className="flex gap-4 max-w-3xl mx-auto">
                            <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center shrink-0">
                                <div className="w-4 h-4 bg-cyan-500 rounded-full animate-pulse" />
                            </div>
                            <div className="space-y-3 w-full">
                                <div className="text-sm font-bold text-cyan-400">WEION Core</div>
                                {/* Thought Process */}
                                <div className="border-l-2 border-slate-700 pl-4 py-1 space-y-2">
                                    <div className="flex items-center gap-2 text-xs text-slate-500">
                                        <span className="w-1.5 h-1.5 rounded-full bg-yellow-500" />
                                        Reading &apos;competitor_analysis_2024.pdf&apos;...
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-slate-500">
                                        <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                                        Identifying key threats and opportunities...
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-slate-500">
                                        <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                                        Drafting strategy document...
                                    </div>
                                </div>
                                <div className="text-slate-300 text-sm leading-relaxed">
                                    I&apos;ve analyzed the report. Key threat identified: Competitor X is lowering prices in the APAC region.
                                    <br /><br />
                                    Here is a proposed counter-strategy:
                                </div>
                                {/* Artifact Card */}
                                <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex items-center justify-between group cursor-pointer hover:border-cyan-500/50 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-slate-900 rounded border border-slate-800">
                                            <span className="text-xs font-bold text-cyan-400">DOC</span>
                                        </div>
                                        <div>
                                            <div className="text-sm font-medium text-white group-hover:text-cyan-400 transition-colors">Q3_Counter_Strategy_Draft.md</div>
                                            <div className="text-xs text-slate-500">Created just now • 2.4 KB</div>
                                        </div>
                                    </div>
                                    <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">
                                        View
                                    </Button>
                                </div>
                            </div>
                        </div>

                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-slate-900 border-t border-slate-800">
                        <div className="max-w-3xl mx-auto relative">
                            <div className="absolute left-2 bottom-2.5 flex gap-1">
                                <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-white">
                                    <Paperclip className="w-4 h-4" />
                                </Button>
                            </div>
                            <div className="absolute right-2 bottom-2.5 flex gap-1">
                                <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-white">
                                    <Mic className="w-4 h-4" />
                                </Button>
                                <Button size="icon" className="h-8 w-8 bg-cyan-600 hover:bg-cyan-700 text-white">
                                    <Send className="w-3 h-3" />
                                </Button>
                            </div>
                            <textarea
                                className="w-full bg-slate-800 border-none rounded-xl py-3 pl-12 pr-24 text-sm text-white placeholder-slate-500 focus:ring-2 focus:ring-cyan-500/50 outline-none resize-none min-h-[50px] max-h-[200px]"
                                placeholder="Ask me to plan or execute a mission..."
                                rows={1}
                            />
                        </div>
                        <div className="text-center mt-2 text-[10px] text-slate-600">
                            WEION can make mistakes. Please verify critical autonomous actions.
                        </div>
                    </div>
                </Card>
            </div>
        </DashboardShell>
    );
}
