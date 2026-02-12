"use client";

import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import {
    X,
    Target,
    Calendar,
    Flag,
    Loader2,
    CheckCircle2,
    Play,
    Pause,
    MessageSquare,
    Paperclip,
    Download
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { formatFileSize, getFileDownloadUrl } from "@/lib/file-upload";
import { generateEnhancedResponse } from "@/lib/response-formatter";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Mission {
    id: string;
    title: string;
    description: string;
    status: "active" | "completed" | "paused" | "failed";
    priority: "low" | "medium" | "high";
    progress: number;
    created_at: string;
    updated_at: string;
}

interface MissionFile {
    id: string;
    filename: string;
    file_size: number;
    storage_path: string;
    mime_type: string;
}

interface MissionUpdate {
    id: string;
    message: string;
    progress: number;
    created_at: string;
}

interface MissionDetailViewProps {
    user: User;
    missionId: string;
    onClose: () => void;
}

export function MissionDetailView({ user, missionId, onClose }: MissionDetailViewProps) {
    const supabase = createClient();
    const [mission, setMission] = useState<Mission | null>(null);
    const [files, setFiles] = useState<MissionFile[]>([]);
    const [updates, setUpdates] = useState<MissionUpdate[]>([]);
    const [isExecuting, setIsExecuting] = useState(false);
    const [aiOutput, setAiOutput] = useState<string>("");
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadMissionDetails();
        loadMissionFiles();
        loadMissionUpdates();

        // Subscribe to mission updates
        const channel = supabase
            .channel(`mission-${missionId}`)
            .on(
                "postgres_changes",
                {
                    event: "UPDATE",
                    schema: "public",
                    table: "missions",
                    filter: `id=eq.${missionId}`,
                },
                () => {
                    loadMissionDetails();
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [missionId]);

    const loadMissionDetails = async () => {
        setIsLoading(true);
        const { data, error } = await supabase
            .from("missions")
            .select("*")
            .eq("id", missionId)
            .single();

        if (!error && data) {
            setMission(data);
        }
        setIsLoading(false);
    };

    const loadMissionFiles = async () => {
        const { data, error } = await supabase
            .from("files")
            .select("*")
            .eq("mission_id", missionId);

        if (!error && data) {
            setFiles(data);
        }
    };

    const loadMissionUpdates = async () => {
        const { data, error } = await supabase
            .from("mission_updates")
            .select("*")
            .eq("mission_id", missionId)
            .order("created_at", { ascending: false });

        if (!error && data) {
            setUpdates(data);
        }
    };

    const startMissionExecution = async () => {
        if (!mission) return;

        setIsExecuting(true);
        setAiOutput("");

        try {
            // Simulate AI thinking and working on the mission
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Generate AI response based on mission
            const response = generateEnhancedResponse(
                `Execute this mission: ${mission.title}. ${mission.description}`
            );

            // Simulate progressive updates
            for (let i = 0; i <= 100; i += 10) {
                await new Promise(resolve => setTimeout(resolve, 500));

                // Update progress
                await supabase
                    .from("missions")
                    .update({ progress: i })
                    .eq("id", missionId);

                // Add update log
                const updateMessage = i === 100
                    ? "Mission execution completed successfully!"
                    : `Processing... ${i}% complete`;

                await supabase
                    .from("mission_updates")
                    .insert({
                        mission_id: missionId,
                        user_id: user.id,
                        message: updateMessage,
                        progress: i,
                    });

                if (i === 100) {
                    setAiOutput(response.response);

                    // Mark as completed
                    await supabase
                        .from("missions")
                        .update({
                            status: "completed",
                            progress: 100
                        })
                        .eq("id", missionId);
                }
            }

            loadMissionUpdates();
        } catch (error) {
            console.error("Error executing mission:", error);

            await supabase
                .from("mission_updates")
                .insert({
                    mission_id: missionId,
                    user_id: user.id,
                    message: "Mission execution failed: " + (error as Error).message,
                    progress: mission.progress,
                });
        } finally {
            setIsExecuting(false);
        }
    };

    const pauseMission = async () => {
        await supabase
            .from("missions")
            .update({ status: "paused" })
            .eq("id", missionId);

        await supabase
            .from("mission_updates")
            .insert({
                mission_id: missionId,
                user_id: user.id,
                message: "Mission paused by user",
                progress: mission?.progress || 0,
            });

        loadMissionDetails();
        loadMissionUpdates();
    };

    const handleFileDownload = async (file: MissionFile) => {
        try {
            const url = await getFileDownloadUrl(file.storage_path);
            if (url) {
                window.open(url, "_blank");
            }
        } catch (error) {
            console.error("Error downloading file:", error);
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case "high":
                return "text-red-400 bg-red-500/10";
            case "medium":
                return "text-yellow-400 bg-yellow-500/10";
            case "low":
                return "text-green-400 bg-green-500/10";
            default:
                return "text-slate-400 bg-slate-500/10";
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case "active":
                return "text-cyan-400 bg-cyan-500/10";
            case "completed":
                return "text-green-400 bg-green-500/10";
            case "paused":
                return "text-yellow-400 bg-yellow-500/10";
            case "failed":
                return "text-red-400 bg-red-500/10";
            default:
                return "text-slate-400 bg-slate-500/10";
        }
    };

    if (isLoading || !mission) {
        return (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                <div className="bg-slate-900 rounded-lg p-8">
                    <Loader2 className="w-8 h-8 text-cyan-500 animate-spin" />
                </div>
            </div>
        );
    }

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-900 rounded-lg border border-slate-700 w-full max-w-4xl max-h-[90vh] flex flex-col">
                {/* Header */}
                <div className="p-6 border-b border-slate-700">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <Target className="w-6 h-6 text-cyan-500" />
                                <h2 className="text-2xl font-bold text-white break-words">
                                    {mission.title}
                                </h2>
                            </div>
                            <p className="text-slate-400 text-sm break-words">
                                {mission.description}
                            </p>
                        </div>
                        <button
                            onClick={onClose}
                            className="ml-4 text-slate-400 hover:text-white transition-colors"
                        >
                            <X className="w-6 h-6" />
                        </button>
                    </div>

                    {/* Meta Info */}
                    <div className="flex items-center gap-4 mt-4">
                        <span className={`px-3 py-1 rounded text-xs font-medium ${getStatusColor(mission.status)}`}>
                            {mission.status.toUpperCase()}
                        </span>
                        <span className={`px-3 py-1 rounded text-xs font-medium ${getPriorityColor(mission.priority)}`}>
                            <Flag className="w-3 h-3 inline mr-1" />
                            {mission.priority.toUpperCase()}
                        </span>
                        <span className="text-xs text-slate-500">
                            <Calendar className="w-3 h-3 inline mr-1" />
                            Created {new Date(mission.created_at).toLocaleDateString()}
                        </span>
                    </div>

                    {/* Progress Bar */}
                    <div className="mt-4">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-slate-400">Progress</span>
                            <span className="text-sm font-medium text-cyan-400">{mission.progress}%</span>
                        </div>
                        <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-500"
                                style={{ width: `${mission.progress}%` }}
                            />
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex items-center gap-3 mt-4">
                        {mission.status !== "completed" && (
                            <>
                                {mission.status !== "paused" ? (
                                    <>
                                        <Button
                                            onClick={startMissionExecution}
                                            disabled={isExecuting}
                                            className="bg-cyan-600 hover:bg-cyan-700 text-white"
                                        >
                                            {isExecuting ? (
                                                <>
                                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                    Executing...
                                                </>
                                            ) : (
                                                <>
                                                    <Play className="w-4 h-4 mr-2" />
                                                    Start Execution
                                                </>
                                            )}
                                        </Button>
                                        <Button
                                            onClick={pauseMission}
                                            disabled={isExecuting}
                                            variant="outline"
                                            className="border-slate-700 text-slate-300 hover:bg-slate-800"
                                        >
                                            <Pause className="w-4 h-4 mr-2" />
                                            Pause
                                        </Button>
                                    </>
                                ) : (
                                    <Button
                                        onClick={startMissionExecution}
                                        className="bg-cyan-600 hover:bg-cyan-700 text-white"
                                    >
                                        <Play className="w-4 h-4 mr-2" />
                                        Resume
                                    </Button>
                                )}
                            </>
                        )}
                        {mission.status === "completed" && (
                            <div className="flex items-center gap-2 text-green-400">
                                <CheckCircle2 className="w-5 h-5" />
                                <span className="font-medium">Mission Completed!</span>
                            </div>
                        )}
                    </div>
                </div>

                {/* Content Area */}
                <ScrollArea className="flex-1 p-6">
                    <div className="space-y-6">
                        {/* Attached Files */}
                        {files.length > 0 && (
                            <div>
                                <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                                    <Paperclip className="w-4 h-4" />
                                    Reference Files ({files.length})
                                </h3>
                                <div className="space-y-2">
                                    {files.map((file) => (
                                        <div
                                            key={file.id}
                                            className="flex items-center gap-3 p-3 bg-slate-800 rounded-lg border border-slate-700 hover:border-cyan-500/50 transition-colors"
                                        >
                                            <Paperclip className="w-4 h-4 text-slate-400" />
                                            <div className="flex-1 min-w-0">
                                                <p className="text-sm text-white truncate">{file.filename}</p>
                                                <p className="text-xs text-slate-500">
                                                    {formatFileSize(file.file_size)}
                                                </p>
                                            </div>
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                onClick={() => handleFileDownload(file)}
                                                className="shrink-0"
                                            >
                                                <Download className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* AI Output */}
                        {aiOutput && (
                            <div>
                                <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                                    <Target className="w-4 h-4" />
                                    Mission Output
                                </h3>
                                <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
                                    <div className="prose prose-sm prose-invert max-w-none">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {aiOutput}
                                        </ReactMarkdown>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Mission Updates */}
                        <div>
                            <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                                <MessageSquare className="w-4 h-4" />
                                Activity Log ({updates.length})
                            </h3>
                            <div className="space-y-2">
                                {updates.length === 0 ? (
                                    <p className="text-sm text-slate-500 text-center py-4">
                                        No activity yet. Start execution to begin.
                                    </p>
                                ) : (
                                    updates.map((update) => (
                                        <div
                                            key={update.id}
                                            className="flex items-start gap-3 p-3 bg-slate-800/50 rounded-lg"
                                        >
                                            <div className="w-1 h-1 rounded-full bg-cyan-500 mt-2" />
                                            <div className="flex-1">
                                                <p className="text-sm text-slate-300 break-words">
                                                    {update.message}
                                                </p>
                                                <p className="text-xs text-slate-500 mt-1">
                                                    {new Date(update.created_at).toLocaleString()} • {update.progress}%
                                                </p>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                </ScrollArea>
            </div>
        </div>
    );
}
