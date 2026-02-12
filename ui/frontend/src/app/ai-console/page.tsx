"use client";

import { useState, useEffect } from "react";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import { AIChatConsole } from "@/components/ai-console/AIChatConsole";
import { MissionsSidebar } from "@/components/ai-console/MissionsSidebar";
import { ProjectsSidebar } from "@/components/ai-console/ProjectsSidebar";
import { ChatHistory } from "@/components/ai-console/ChatHistory";
import { MissionDialog } from "@/components/ai-console/MissionDialog";
import { ProjectDialog } from "@/components/ai-console/ProjectDialog";
import { MissionDetailView } from "@/components/ai-console/MissionDetailView";
import { Button } from "@/components/ui/button";
import { Plus, Target } from "lucide-react";

export default function AIConsolePage() {
    const supabase = createClient();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedChatId, setSelectedChatId] = useState<string | null>(null);
    const [chatRefreshTrigger, setChatRefreshTrigger] = useState(0);
    const [isMissionDialogOpen, setIsMissionDialogOpen] = useState(false);
    const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false);
    const [selectedMissionId, setSelectedMissionId] = useState<string | null>(null);

    useEffect(() => {
        const checkUser = async () => {
            const {
                data: { user },
            } = await supabase.auth.getUser();

            if (!user) {
                redirect("/login");
            }

            setUser(user);
            setLoading(false);
        };

        checkUser();
    }, []);

    const handleChatCreated = (chatId: string) => {
        setSelectedChatId(chatId);
        setChatRefreshTrigger((prev) => prev + 1);
    };

    const handleMissionSuccess = () => {
        // Missions sidebar will auto-refresh via realtime subscription
    };

    const handleProjectSuccess = () => {
        // Projects sidebar will auto-refresh via realtime subscription
    };

    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-slate-950">
                <div className="text-cyan-500">Loading...</div>
            </div>
        );
    }

    if (!user) {
        return null;
    }

    return (
        <div className="h-screen flex bg-slate-950">
            {/* Unified Sidebar */}
            <div className="w-64 border-r border-slate-800 flex flex-col bg-slate-950/50">
                {/* Sidebar Header */}
                <div className="p-4 border-b border-slate-800">
                    <h1 className="text-xl font-bold text-white mb-1 break-words">Mission Control</h1>
                    <p className="text-xs text-slate-500">Advanced AI Console</p>
                </div>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto">
                    <div className="p-4 space-y-4">
                        {/* Missions Section */}
                        <MissionsSidebar
                            user={user}
                            onSelectMission={(missionId) => setSelectedMissionId(missionId)}
                        />

                        {/* Projects Section */}
                        <ProjectsSidebar
                            user={user}
                            onCreateProject={() => setIsProjectDialogOpen(true)}
                        />

                        {/* Chats Section */}
                        <ChatHistory
                            user={user}
                            selectedChatId={selectedChatId}
                            onSelectChat={setSelectedChatId}
                            onChatCreated={() => setChatRefreshTrigger((prev) => prev + 1)}
                        />
                    </div>
                </div>

                {/* Bottom Actions */}
                <div className="p-4 border-t border-slate-800 space-y-2">
                    <Button
                        onClick={() => setSelectedChatId(null)}
                        className="w-full bg-cyan-600 hover:bg-cyan-700 text-white justify-start"
                        size="sm"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        New Chat
                    </Button>
                    <Button
                        onClick={() => setIsMissionDialogOpen(true)}
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white justify-start"
                        size="sm"
                    >
                        <Target className="w-4 h-4 mr-2" />
                        New Mission
                    </Button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1">
                <AIChatConsole user={user} chatId={selectedChatId} onChatCreated={handleChatCreated} />
            </div>

            {/* Dialogs */}
            <MissionDialog
                user={user}
                isOpen={isMissionDialogOpen}
                onClose={() => setIsMissionDialogOpen(false)}
                onSuccess={handleMissionSuccess}
            />
            <ProjectDialog
                user={user}
                isOpen={isProjectDialogOpen}
                onClose={() => setIsProjectDialogOpen(false)}
                onSuccess={handleProjectSuccess}
            />

            {/* Mission Detail View */}
            {selectedMissionId && (
                <MissionDetailView
                    user={user}
                    missionId={selectedMissionId}
                    onClose={() => setSelectedMissionId(null)}
                />
            )}
        </div>
    );
}
