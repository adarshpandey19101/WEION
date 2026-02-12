"use client";

import { ReactNode } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { User } from "@supabase/supabase-js";

interface DashboardShellProps {
    children: ReactNode;
    user?: User;
}

export function DashboardShell({ children, user }: DashboardShellProps) {
    return (
        <div className="flex h-screen bg-background font-sans text-foreground">
            {/* Sidebar - Fixed width */}
            <Sidebar />

            {/* Main Content Area */}
            <div className="flex flex-1 flex-col overflow-hidden bg-background">
                {/* Topbar */}
                <Topbar user={user} />

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-8">
                    <div className="mx-auto max-w-6xl space-y-8 fade-in">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
