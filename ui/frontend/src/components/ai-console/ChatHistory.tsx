"use client";

import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import { MessageSquare, ChevronDown, MoreHorizontal, Check, X } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
// import { toast } from "sonner"; // Disabled until module available
import ChatActionsMenu from "./ChatActionsMenu";

interface Chat {
    id: string;
    title: string;
    created_at: string;
    project_id?: string | null;
    pinned?: boolean;
}

interface Project {
    id: string;
    name: string;
}

interface ChatHistoryProps {
    user: User;
    selectedChatId: string | null;
    onSelectChat: (chatId: string | null) => void;
    onChatCreated?: () => void;
}

interface MenuState {
    id: string;
    x: number;
    y: number;
}

export function ChatHistory({ user, selectedChatId, onSelectChat, onChatCreated }: ChatHistoryProps) {
    const supabase = createClient();
    const [chats, setChats] = useState<Chat[]>([]);
    const [projects, setProjects] = useState<Project[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isExpanded, setIsExpanded] = useState(true);

    // Menu State - Changed to include position
    const [activeMenu, setActiveMenu] = useState<MenuState | null>(null);
    const [renamingId, setRenamingId] = useState<string | null>(null);
    const [renameValue, setRenameValue] = useState("");

    // Initial Fetch
    useEffect(() => {
        fetchChats();
        fetchProjects();
    }, []);

    // Refresh when parent signals new chat created
    useEffect(() => {
        if (onChatCreated) {
            fetchChats();
        }
    }, [onChatCreated]);

    // Global Keyboard Shortcuts
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (!selectedChatId) return;

            // Cmd + Backspace -> Delete
            if ((e.metaKey || e.ctrlKey) && e.key === 'Backspace') {
                e.preventDefault();
                const el = document.activeElement as HTMLElement;
                const rect = el?.getBoundingClientRect();
                if (rect) {
                    setActiveMenu({ id: selectedChatId, x: rect.right, y: rect.top });
                }
            }

            // Cmd + R -> Rename
            if ((e.metaKey || e.ctrlKey) && e.key === 'r') {
                e.preventDefault();
                const chat = chats.find(c => c.id === selectedChatId);
                if (chat) startRenaming(chat);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [selectedChatId, chats]);

    const fetchChats = async () => {
        setIsLoading(true);
        try {
            let query = supabase
                .from("chats")
                .select("*")
                .eq("user_id", user.id)
                .is("project_id", null);

            const { data, error } = await query.order("created_at", { ascending: false });

            if (error) throw error;

            let fetchedChats = data || [];

            // Sort: Pinned first, then Date
            fetchedChats.sort((a, b) => {
                if (a.pinned && !b.pinned) return -1;
                if (!a.pinned && b.pinned) return 1;
                return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
            });

            setChats(fetchedChats);
        } catch (error) {
            console.error("Error fetching chats:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchProjects = async () => {
        try {
            const { data, error } = await supabase
                .from("projects")
                .select("id, name")
                .eq("user_id", user.id)
                .order("created_at", { ascending: false });

            if (!error && data) {
                setProjects(data);
            }
        } catch (error) {
            console.error("Error fetching projects:", error);
        }
    };

    const dispatchUpdate = () => {
        if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('chat-update'));
        }
    };

    const handlePin = async (chatId: string, isPinned: boolean) => {
        setChats(current => {
            const updated = current.map(c => c.id === chatId ? { ...c, pinned: isPinned } : c);
            return updated.sort((a, b) => {
                if (a.pinned && !b.pinned) return -1;
                if (!a.pinned && b.pinned) return 1;
                return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
            });
        });

        try {
            await supabase.from("chats").update({ pinned: isPinned }).eq("id", chatId);
            dispatchUpdate();
        } catch (error) {
            console.error("Error updating pin state:", error);
            fetchChats();
        }
    };

    const handleShare = (chatId: string) => {
        try {
            const url = `${window.location.origin}/share/chat/${chatId}`;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url)
                    .then(() => alert("Link copied to clipboard: " + url))
                    .catch(err => {
                        console.error("Clipboard write failed:", err);
                        alert("Could not copy link. URL: " + url);
                    });
            } else {
                alert("Link: " + url);
            }
        } catch (e) {
            console.error("Share error:", e);
        }
    };

    const moveChatToProject = async (chatId: string, projectId: string) => {
        try {
            const { error } = await supabase
                .from("chats")
                .update({ project_id: projectId })
                .eq("id", chatId);

            if (!error) {
                fetchChats();
                setActiveMenu(null);
                dispatchUpdate();
            }
        } catch (error) {
            console.error("Error moving chat:", error);
        }
    };

    const createProject = async (name: string): Promise<string | null> => {
        try {
            const { data, error } = await supabase
                .from("projects")
                .insert({
                    user_id: user.id,
                    name: name.trim(),
                    status: "active",
                    color: "#8b5cf6"
                })
                .select()
                .single();

            if (error) throw error;
            if (data) {
                fetchProjects();
                dispatchUpdate();
                return data.id;
            }
        } catch (error) {
            console.error("Error creating project:", error);
        }
        return null;
    };

    const handleRename = async (chatId: string, newTitle: string) => {
        if (!newTitle.trim()) return;

        try {
            const { error } = await supabase
                .from("chats")
                .update({ title: newTitle.trim() })
                .eq("id", chatId);

            if (!error) {
                setChats(chats.map(c => c.id === chatId ? { ...c, title: newTitle.trim() } : c));
                setRenamingId(null);
                setRenameValue("");
                dispatchUpdate();
            }
        } catch (error) {
            console.error("Error renaming chat:", error);
        }
    };

    const handleDelete = async (chatId: string) => {
        try {
            const { error: softDeleteError } = await supabase
                .from("chats")
                .update({ deleted_at: new Date().toISOString() })
                .eq("id", chatId);

            if (softDeleteError) {
                await supabase.from("chats").delete().eq("id", chatId);
            }

            setChats(chats.filter(c => c.id !== chatId));
            setActiveMenu(null);
            if (selectedChatId === chatId) {
                onSelectChat(null);
            }
            dispatchUpdate();
        } catch (error) {
            console.error("Error deleting chat:", error);
        }
    };

    const startRenaming = (chat: Chat) => {
        setRenamingId(chat.id);
        setRenameValue(chat.title || "New conversation");
        setActiveMenu(null);
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

        if (diffInHours < 24) {
            return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        } else if (diffInHours < 168) {
            return date.toLocaleDateString([], { weekday: "short" });
        } else {
            return date.toLocaleDateString([], { month: "short", day: "numeric" });
        }
    };

    return (
        <div className="w-80 border-r border-slate-800 bg-slate-950/50 flex flex-col relative">
            <ScrollArea className="flex-1">
                <div className="p-2 space-y-1">
                    {isLoading ? (
                        <div className="text-center py-8 text-slate-500 text-sm">Loading conversations...</div>
                    ) : chats.length === 0 ? (
                        <div className="text-center py-8 text-slate-500 text-sm">No conversations yet</div>
                    ) : (
                        <>
                            <button
                                onClick={() => setIsExpanded(!isExpanded)}
                                className="w-full flex items-center justify-between px-4 py-2 hover:bg-slate-800/50 transition-colors rounded"
                            >
                                <div className="flex items-center gap-2">
                                    <ChevronDown className={cn("w-4 h-4 text-slate-400 transition-transform", !isExpanded && "-rotate-90")} />
                                    <MessageSquare className="w-4 h-4 text-slate-400" />
                                    <span className="font-semibold text-white text-sm uppercase tracking-wide">CHATS</span>
                                </div>
                                <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">{chats.length}</span>
                            </button>

                            {isExpanded && (
                                <div className="space-y-1 mt-2">
                                    {chats.map((chat) => (
                                        <div
                                            key={chat.id}
                                            className="relative group"
                                            onContextMenu={(e) => {
                                                e.preventDefault();
                                                e.stopPropagation(); // Stop propagation to avoid bubbling issues
                                                const x = Math.min(e.clientX, window.innerWidth - 240); // 240px approx width
                                                const y = Math.min(e.clientY, window.innerHeight - 300); // 300px approx max height
                                                setActiveMenu({ id: chat.id, x, y });
                                            }}
                                        >
                                            <div className="flex items-center gap-1">
                                                <div
                                                    role="button"
                                                    tabIndex={0}
                                                    onClick={() => onSelectChat(chat.id)}
                                                    onKeyDown={(e) => {
                                                        if (e.key === 'Enter' || e.key === ' ') {
                                                            e.preventDefault();
                                                            onSelectChat(chat.id);
                                                        }
                                                    }}
                                                    className={cn(
                                                        "flex-1 text-left p-3 rounded-lg transition-colors cursor-pointer outline-none focus:ring-2 focus:ring-cyan-500/50",
                                                        selectedChatId === chat.id
                                                            ? "bg-slate-800 text-white"
                                                            : "text-slate-400 hover:bg-slate-900/50 hover:text-slate-300"
                                                    )}
                                                >
                                                    <div className="flex items-start gap-3">
                                                        <MessageSquare className={cn("w-4 h-4 mt-0.5 shrink-0", chat.pinned ? "text-cyan-400 fill-cyan-400/20" : "")} />
                                                        <div className="flex-1 min-w-0 pr-2">
                                                            {renamingId === chat.id ? (
                                                                <div className="flex items-center gap-1" onClick={e => e.stopPropagation()}>
                                                                    <input
                                                                        type="text"
                                                                        value={renameValue}
                                                                        onChange={(e) => setRenameValue(e.target.value)}
                                                                        className="w-full bg-slate-900 border border-slate-700 rounded px-1.5 py-0.5 text-sm text-white focus:outline-none focus:border-cyan-500 min-w-0"
                                                                        autoFocus
                                                                        onKeyDown={(e) => {
                                                                            if (e.key === 'Enter') handleRename(chat.id, renameValue);
                                                                            if (e.key === 'Escape') setRenamingId(null);
                                                                        }}
                                                                    />
                                                                    <button
                                                                        onClick={(e) => {
                                                                            e.stopPropagation();
                                                                            handleRename(chat.id, renameValue);
                                                                        }}
                                                                        className="p-1 hover:bg-slate-700 rounded bg-slate-800"
                                                                    >
                                                                        <Check className="w-3 h-3 text-green-500" />
                                                                    </button>
                                                                    <button
                                                                        onClick={(e) => {
                                                                            e.stopPropagation();
                                                                            setRenamingId(null);
                                                                        }}
                                                                        className="p-1 hover:bg-slate-700 rounded bg-slate-800"
                                                                    >
                                                                        <X className="w-3 h-3 text-red-500" />
                                                                    </button>
                                                                </div>
                                                            ) : (
                                                                <p className="text-sm font-medium break-words line-clamp-2">
                                                                    {chat.title || "New conversation"}
                                                                </p>
                                                            )}
                                                            <div className="flex items-center gap-2 mt-0.5">
                                                                <p className="text-xs text-slate-500">
                                                                    {formatDate(chat.created_at)}
                                                                </p>
                                                                {chat.pinned && (
                                                                    <span className="text-[10px] bg-cyan-950/50 text-cyan-500 px-1 rounded border border-cyan-900/50">
                                                                        PINNED
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        // Calculate position based on the button rect
                                                        const rect = e.currentTarget.getBoundingClientRect();
                                                        const x = Math.min(rect.left, window.innerWidth - 240);
                                                        const y = Math.min(rect.bottom + 5, window.innerHeight - 300);
                                                        setActiveMenu({ id: chat.id, x, y });
                                                    }}
                                                    className={cn(
                                                        "p-2 hover:bg-slate-800 rounded transition-colors",
                                                        activeMenu?.id === chat.id ? "opacity-100 bg-slate-800" : "opacity-0 group-hover:opacity-100 focus:opacity-100"
                                                    )}
                                                >
                                                    <MoreHorizontal className="w-4 h-4 text-slate-500 hover:text-slate-300" />
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </div>
            </ScrollArea>

            {/* Render Menu outside ScrollArea with fixed positioning */}
            {activeMenu && chats.find(c => c.id === activeMenu.id) && (
                <ChatActionsMenu
                    chat={chats.find(c => c.id === activeMenu.id)!}
                    projects={projects}
                    onClose={() => setActiveMenu(null)}
                    onRename={() => startRenaming(chats.find(c => c.id === activeMenu.id)!)}
                    onDelete={handleDelete}
                    onMoveToProject={moveChatToProject}
                    onCreateProject={createProject}
                    onPin={handlePin}
                    onShare={handleShare}
                    position={{ x: activeMenu.x, y: activeMenu.y }}
                />
            )}
        </div>
    );
}
