"use client";

import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import { ChevronDown, ChevronRight, Target, CheckCircle2, Pause, XCircle, Circle, CheckCircle } from "lucide-react";

interface Mission {
    id: string;
    title: string;
    description: string;
    status: "active" | "completed" | "paused" | "failed";
    priority: "low" | "medium" | "high";
    progress: number;
    created_at: string;
}

interface MissionsSidebarProps {
    user: User;
    onSelectMission?: (missionId: string) => void;
}

export function MissionsSidebar({ user, onSelectMission }: MissionsSidebarProps) {
    const supabase = createClient();
    const [missions, setMissions] = useState<Mission[]>([]);
    const [isExpanded, setIsExpanded] = useState(true);
    const [selectedStatus, setSelectedStatus] = useState<string | null>(null);

    useEffect(() => {
        loadMissions();

        // Subscribe to mission changes
        const channel = supabase
            .channel("missions-changes")
            .on(
                "postgres_changes",
                {
                    event: "*",
                    schema: "public",
                    table: "missions",
                    filter: `user_id=eq.${user.id}`,
                },
                () => {
                    loadMissions();
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [user.id]);

    const loadMissions = async () => {
        const { data, error } = await supabase
            .from("missions")
            .select("*")
            .eq("user_id", user.id)
            .order("created_at", { ascending: false });

        if (!error && data) {
            setMissions(data);
        }
    };

    const toggleMissionStatus = async (missionId: string, currentStatus: string) => {
        const newStatus = currentStatus === "completed" ? "active" : "completed";
        const newProgress = newStatus === "completed" ? 100 : 0;

        const { error } = await supabase
            .from("missions")
            .update({
                status: newStatus,
                progress: newProgress
            })
            .eq("id", missionId);

        if (!error) {
            loadMissions();
        }
    };

    const getMissionsByStatus = (status: string) => {
        return missions.filter((m) => m.status === status);
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "active":
                return <Target className="w-4 h-4 text-cyan-500" />;
            case "completed":
                return <CheckCircle2 className="w-4 h-4 text-green-500" />;
            case "paused":
                return <Pause className="w-4 h-4 text-yellow-500" />;
            case "failed":
                return <XCircle className="w-4 h-4 text-red-500" />;
            default:
                return <Target className="w-4 h-4 text-slate-500" />;
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case "high":
                return "text-red-400";
            case "medium":
                return "text-yellow-400";
            case "low":
                return "text-green-400";
            default:
                return "text-slate-400";
        }
    };

    const activeMissions = getMissionsByStatus("active");
    const completedMissions = getMissionsByStatus("completed");

    return (
        <div className="border-b border-slate-800 pb-4">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-2 hover:bg-slate-800/50 rounded transition-colors"
            >
                <div className="flex items-center gap-2">
                    {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-slate-400" />
                    ) : (
                        <ChevronRight className="w-4 h-4 text-slate-400" />
                    )}
                    <Target className="w-5 h-5 text-cyan-500" />
                    <span className="font-semibold text-white text-sm uppercase tracking-wide">
                        Missions
                    </span>
                </div>
                <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
                    {missions.length}
                </span>
            </button>

            {isExpanded && (
                <div className="mt-2 space-y-1">
                    {/* Active Missions */}
                    {activeMissions.length > 0 && (
                        <div>
                            <div className="px-4 py-1 text-xs font-medium text-slate-500 uppercase tracking-wide">
                                Active ({activeMissions.length})
                            </div>
                            {activeMissions.map((mission) => (
                                <div
                                    key={mission.id}
                                    className="w-full px-4 py-2 hover:bg-slate-800 transition-colors text-left group"
                                >
                                    <div className="flex items-start gap-2">
                                        {/* Complete/Uncomplete checkbox button */}
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                toggleMissionStatus(mission.id, mission.status);
                                            }}
                                            className="mt-0.5 shrink-0 hover:scale-110 transition-transform"
                                            title="Mark as complete"
                                        >
                                            <Circle className="w-4 h-4 text-slate-600 hover:text-cyan-500" />
                                        </button>
                                        {getStatusIcon(mission.status)}
                                        <div
                                            className="flex-1 min-w-0 cursor-pointer"
                                            onClick={() => onSelectMission?.(mission.id)}
                                        >
                                            <div className="text-sm text-white break-words group-hover:text-cyan-400 transition-colors line-clamp-2">
                                                {mission.title}
                                            </div>
                                            <div className="text-xs text-slate-500 break-words line-clamp-1">
                                                {mission.description}
                                            </div>
                                            <div className="flex items-center gap-2 mt-1">
                                                <div className="w-full bg-slate-700 h-1 rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full bg-cyan-500 transition-all"
                                                        style={{ width: `${mission.progress}%` }}
                                                    />
                                                </div>
                                                <span className="text-[10px] text-slate-600">
                                                    {mission.progress}%
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-1 mt-1">
                                                <span
                                                    className={`text-[10px] font-medium ${getPriorityColor(
                                                        mission.priority
                                                    )}`}
                                                >
                                                    {mission.priority.toUpperCase()}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Completed Missions */}
                    {completedMissions.length > 0 && (
                        <div>
                            <div className="px-4 py-1 text-xs font-medium text-slate-500 uppercase tracking-wide">
                                Completed ({completedMissions.length})
                            </div>
                            {completedMissions.slice(0, 3).map((mission) => (
                                <div
                                    key={mission.id}
                                    className="w-full px-4 py-2 hover:bg-slate-800 transition-colors text-left opacity-60 hover:opacity-100"
                                >
                                    <div className="flex items-start gap-2">
                                        {/* Complete/Uncomplete checkbox button */}
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                toggleMissionStatus(mission.id, mission.status);
                                            }}
                                            className="mt-0.5 shrink-0 hover:scale-110 transition-transform"
                                            title="Mark as active"
                                        >
                                            <CheckCircle className="w-4 h-4 text-green-500 hover:text-slate-400" />
                                        </button>
                                        {getStatusIcon(mission.status)}
                                        <div
                                            className="flex-1 min-w-0 cursor-pointer"
                                            onClick={() => onSelectMission?.(mission.id)}
                                        >
                                            <div className="text-sm text-white break-words line-through line-clamp-2">
                                                {mission.title}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {missions.length === 0 && (
                        <div className="px-4 py-3 text-xs text-slate-500 text-center">
                            No missions yet. Create one to get started.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
