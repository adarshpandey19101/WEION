import {
    Pin,
    Pencil,
    FolderInput,
    Share2,
    Trash2,
    X,
    Check,
    Plus,
    ArrowLeft
} from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";

interface Project {
    id: string;
    name: string;
}

interface Chat {
    id: string;
    title: string;
    pinned?: boolean;
}

interface ChatActionsMenuProps {
    chat: Chat;
    projects: Project[];
    onClose: () => void;
    onRename: (id: string, newTitle: string) => void;
    onDelete: (id: string) => void;
    onMoveToProject: (chatId: string, projectId: string) => void;
    onCreateProject: (name: string) => Promise<string | null>; // Returns new projectId
    onPin: (id: string, isPinned: boolean) => void;
    onShare: (id: string) => void;
    position?: { x: number; y: number };
}

export default function ChatActionsMenu({
    chat,
    projects,
    onClose,
    onRename,
    onDelete,
    onMoveToProject,
    onCreateProject,
    onPin,
    onShare,
    position
}: ChatActionsMenuProps) {
    const [view, setView] = useState<"main" | "projects" | "create_project" | "delete_confirm">("main");
    const [newProjectName, setNewProjectName] = useState("");
    const menuRef = useRef<HTMLDivElement>(null);

    // Close on click outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                onClose();
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [onClose]);

    const handleCreateProject = async () => {
        if (!newProjectName.trim()) return;
        const projectId = await onCreateProject(newProjectName);
        if (projectId) {
            onMoveToProject(chat.id, projectId);
            onClose();
        }
    };

    const MenuItem = ({ icon, label, onClick, danger = false }: { icon: React.ReactNode, label: string, onClick: () => void, danger?: boolean }) => (
        <button
            onClick={(e) => {
                e.stopPropagation();
                onClick();
            }}
            className={`flex items-center gap-2 w-full px-3 py-2 text-sm text-left transition-colors
                hover:bg-slate-800 rounded-sm
                ${danger ? "text-red-400 hover:text-red-300" : "text-slate-300"}`}
        >
            {icon}
            <span className="flex-1">{label}</span>
        </button>
    );

    return (
        <div
            ref={menuRef}
            className={`
                w-56 bg-slate-900 border border-slate-700 rounded-lg shadow-xl z-50 p-1 animate-in fade-in zoom-in-95 duration-100
                ${position ? "fixed" : "absolute right-2 top-8"}
            `}
            style={position ? { top: position.y, left: position.x } : undefined}
            onClick={(e) => e.stopPropagation()}
        >
            {view === "main" && (
                <div className="flex flex-col gap-0.5">
                    <MenuItem
                        icon={<Pin size={14} className={chat.pinned ? "fill-current" : ""} />}
                        label={chat.pinned ? "Unpin Chat" : "Pin Chat"}
                        onClick={() => {
                            onPin(chat.id, !chat.pinned);
                            onClose();
                        }}
                    />
                    <MenuItem
                        icon={<Pencil size={14} />}
                        label="Rename"
                        onClick={() => {
                            onRename(chat.id, chat.title); // Trigger inline rename in parent
                            onClose();
                        }}
                    />
                    <MenuItem
                        icon={<FolderInput size={14} />}
                        label="Move to Project"
                        onClick={() => setView("projects")}
                    />
                    <MenuItem
                        icon={<Share2 size={14} />}
                        label="Share"
                        onClick={() => {
                            onShare(chat.id);
                            onClose();
                        }}
                    />
                    <div className="h-px bg-slate-800 my-1" />
                    <MenuItem
                        icon={<Trash2 size={14} />}
                        label="Delete"
                        danger
                        onClick={() => setView("delete_confirm")}
                    />
                </div>
            )}

            {view === "projects" && (
                <div className="flex flex-col gap-0.5">
                    <div className="flex items-center px-2 py-1.5 border-b border-slate-800 mb-1">
                        <button
                            onClick={() => setView("main")}
                            className="mr-2 hover:bg-slate-800 rounded p-0.5 text-slate-400 hover:text-white"
                        >
                            <ArrowLeft size={14} />
                        </button>
                        <span className="text-xs text-slate-400 font-medium">Select Project</span>
                    </div>

                    <MenuItem
                        icon={<Plus size={14} className="text-cyan-400" />}
                        label="Create New Project"
                        onClick={() => setView("create_project")}
                    />

                    <div className="max-h-48 overflow-y-auto my-1 custom-scrollbar">
                        {projects.length === 0 ? (
                            <div className="px-3 py-2 text-xs text-slate-500 text-center">No projects yet</div>
                        ) : (
                            projects.map((project) => (
                                <MenuItem
                                    key={project.id}
                                    icon={<FolderInput size={14} className="text-slate-500" />}
                                    label={project.name}
                                    onClick={() => {
                                        onMoveToProject(chat.id, project.id);
                                        onClose();
                                    }}
                                />
                            ))
                        )}
                    </div>
                </div>
            )}

            {view === "create_project" && (
                <div className="p-2">
                    <div className="flex items-center mb-2">
                        <button
                            onClick={() => setView("projects")}
                            className="mr-2 hover:bg-slate-800 rounded p-0.5 text-slate-400"
                        >
                            <ArrowLeft size={14} />
                        </button>
                        <span className="text-xs text-slate-400 font-medium">New Project</span>
                    </div>
                    <input
                        type="text"
                        value={newProjectName}
                        onChange={(e) => setNewProjectName(e.target.value)}
                        placeholder="Project name..."
                        className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-sm text-white focus:outline-none focus:border-cyan-500 mb-2 placeholder:text-slate-600"
                        autoFocus
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') handleCreateProject();
                            if (e.key === 'Escape') setView("projects");
                        }}
                    />
                    <Button
                        size="sm"
                        className="w-full h-8 text-xs bg-cyan-600 hover:bg-cyan-700 text-white"
                        onClick={handleCreateProject}
                    >
                        Create & Move
                    </Button>
                </div>
            )}

            {view === "delete_confirm" && (
                <div className="p-2">
                    <div className="text-xs text-slate-300 mb-3 px-1">
                        Are you sure you want to delete this chat?
                    </div>
                    <div className="flex gap-2">
                        <Button
                            size="sm"
                            variant="destructive"
                            className="flex-1 h-7 text-xs"
                            onClick={() => {
                                onDelete(chat.id);
                                onClose();
                            }}
                        >
                            Delete
                        </Button>
                        <Button
                            size="sm"
                            variant="ghost"
                            className="flex-1 h-7 text-xs hover:bg-slate-800 hover:text-white"
                            onClick={() => setView("main")}
                        >
                            Cancel
                        </Button>
                    </div>
                </div>
            )}
        </div>
    );
}
