"use client";

import { Bell, Search, User } from "lucide-react";

export function Topbar() {
    return (
        <header className="h-14 border-b bg-background px-6 flex items-center justify-between shrink-0">
            {/* Search */}
            <div className="relative w-96">
                <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                    type="text"
                    placeholder="Search missions, artifacts, or memories..."
                    className="w-full bg-muted/50 border-none rounded-md py-1.5 pl-9 pr-4 text-sm focus:ring-1 focus:ring-ring outline-none transition-all placeholder:text-muted-foreground"
                />
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-2">
                <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-muted/50">
                    <Bell className="w-4 h-4" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-600 rounded-full border-2 border-background" />
                </button>

                <div className="h-4 w-px bg-border mx-2" />

                <button className="flex items-center gap-2 pl-2 hover:bg-muted/50 p-1.5 rounded-md transition-colors">
                    <div className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center border">
                        <User className="w-3.5 h-3.5 text-muted-foreground" />
                    </div>
                    <span className="text-xs font-medium hidden md:block">Adarsh Pandey</span>
                </button>
            </div>
        </header>
    );
}
