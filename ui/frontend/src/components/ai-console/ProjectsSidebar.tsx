"use client";

import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import { Folder, ChevronDown, ChevronRight, Plus, MoreHorizontal, MessageSquare, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Project {
    id: string;
    name: string;
    description: string;
    color: string;
    chat_count?: number;
    chats?: Chat[];
    created_at: string;
}

interface Chat {
    id: string;
    title: string;
    created_at: string;
}

interface ProjectsSidebarProps {
    user: User;
    onSelectProject?: (projectId: string) => void;
    onSelectChat?: (chatId: string) => void;
    onCreateProject?: () => void;
}

export function ProjectsSidebar({ user, onSelectProject, onSelectChat, onCreateProject }: ProjectsSidebarProps) {
    const supabase = createClient();
    const [projects, setProjects] = useState<Project[]>([]);
    const [isExpanded, setIsExpanded] = useState(true);
    const [expandedProjects, setExpandedProjects] = useState<Set<string>>(new Set());

    useEffect(() => {
        loadProjects();

        // Custom event for immediate updates from ChatHistory
        const handleChatUpdate = () => {
            loadProjects();
        };

        if (typeof window !== 'undefined') {
            window.addEventListener('chat-update', handleChatUpdate);
        }

        // Subscribe to project changes
        const projectsChannel = supabase
            .channel("projects-changes")
            .on(
                "postgres_changes",
                {
                    event: "*",
                    schema: "public",
                    table: "projects",
                    filter: `user_id=eq.${user.id}`,
                },
                () => {
                    loadProjects();
                }
            )
            .subscribe();

        // Subscribe to chat changes (for counts)
        const chatsChannel = supabase
            .channel("projects-chats-changes")
            .on(
                "postgres_changes",
                {
                    event: "*",
                    schema: "public",
                    table: "chats",
                    filter: `user_id=eq.${user.id}`,
                },
                () => {
                    loadProjects();
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(projectsChannel);
            supabase.removeChannel(chatsChannel);
            if (typeof window !== 'undefined') {
                window.removeEventListener('chat-update', handleChatUpdate);
            }
        };
    }, [user.id]);

    const loadProjects = async () => {
        const { data, error } = await supabase
            .from("projects")
            .select(`
                *,
                chats (
                    id,
                    title,
                    created_at
                )
            `)
            .eq("user_id", user.id)
            .order("updated_at", { ascending: false });

        if (!error && data) {
            // Transform data to include chat_count
            const projectsWithCount = data.map(project => ({
                ...project,
                chat_count: project.chats?.length || 0
            }));
            setProjects(projectsWithCount);
        }
    };

    const toggleProjectExpand = (projectId: string) => {
        setExpandedProjects(prev => {
            const newSet = new Set(prev);
            if (newSet.has(projectId)) {
                newSet.delete(projectId);
            } else {
                newSet.add(projectId);
            }
            return newSet;
        });
    };

    const removeChatFromProject = async (chatId: string) => {
        try {
            const { error } = await supabase
                .from("chats")
                .update({ project_id: null })
                .eq("id", chatId);

            if (!error) {
                loadProjects();
            }
        } catch (error) {
            console.error("Error removing chat from project:", error);
        }
    };

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
                    <Folder className="w-5 h-5 text-purple-500" />
                    <span className="font-semibold text-white text-sm uppercase tracking-wide">
                        Projects
                    </span>
                </div>
                <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
                    {projects.length}
                </span>
            </button>

            {isExpanded && (
                <div className="mt-2 space-y-1">
                    {projects.map((project) => (
                        <button
                            key={project.id}
                            onClick={() => onSelectProject?.(project.id)}
                            className="w-full px-4 py-2 hover:bg-slate-800 transition-colors text-left group flex items-center gap-2"
                        >
                            <Folder
                                className="w-4 h-4 shrink-0"
                                style={{ color: project.color || "#8b5cf6" }}
                            />
                            <div className="flex-1 min-w-0">
                                <div className="text-sm text-white break-words group-hover:text-purple-400 transition-colors line-clamp-2">
                                    {project.name}
                                </div>
                                {project.description && (
                                    <div className="text-xs text-slate-500 break-words line-clamp-1">
                                        {project.description}
                                    </div>
                                )}
                            </div>
                            {project.chat_count && project.chat_count > 0 && (
                                <span className="text-xs text-slate-600 bg-slate-800 px-1.5 py-0.5 rounded">
                                    {project.chat_count}
                                </span>
                            )}
                        </button>
                    ))}

                    {projects.length === 0 && (
                        <div className="px-4 py-3 text-xs text-slate-500 text-center">
                            No projects yet. Create one to organize your chats.
                        </div>
                    )}

                    <Button
                        onClick={onCreateProject}
                        variant="ghost"
                        size="sm"
                        className="w-full justify-start text-xs text-slate-400 hover:text-white hover:bg-slate-800"
                    >
                        <Plus className="w-3 h-3 mr-1" />
                        New Project
                    </Button>
                </div>
            )}
        </div>
    );
}
