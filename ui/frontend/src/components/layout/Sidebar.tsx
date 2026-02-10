"use client";

import {
    LayoutDashboard,
    Bot,
    Target,
    Brain,
    BarChart,
    Cpu,
    Users,
    Settings,
    LogOut,
    ChevronDown
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { OrgSwitcher } from "@/components/layout/OrgSwitcher";

const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/ai-console", label: "MIssions", icon: Bot },
    { href: "/goals", label: "Goals", icon: Target },
    { href: "/memory", label: "Memory", icon: Brain },
    { href: "/analytics", label: "Analytics", icon: BarChart },
    { href: "/simulation", label: "Simulation", icon: Cpu },
    { href: "/governance", label: "Governance", icon: Users },
    { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="w-[280px] border-r bg-sidebar flex flex-col shrink-0">
            {/* Header */}
            <div className="h-16 flex items-center px-6 border-b border-sidebar-border">
                <div className="flex items-center gap-2 font-semibold tracking-tight">
                    <div className="w-6 h-6 bg-foreground text-background rounded-md flex items-center justify-center text-xs font-bold">
                        W
                    </div>
                    <span>WEION</span>
                </div>
            </div>

            {/* Org Switcher / User Profile Area */}
            <div className="p-4">
                <OrgSwitcher />
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
                <div className="text-xs font-medium text-muted-foreground px-2 py-2 mb-2">
                    Platform
                </div>
                {navItems.map((item) => (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={cn(
                            "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                            pathname === item.href
                                ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                                : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-foreground"
                        )}
                    >
                        <item.icon className="w-4 h-4 opacity-70" />
                        {item.label}
                    </Link>
                ))}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-sidebar-border">
                <button className="flex items-center gap-3 px-3 py-2 w-full rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-sidebar-accent/50 transition-colors">
                    <LogOut className="w-4 h-4" />
                    Sign Out
                </button>
            </div>
        </aside>
    );
}
