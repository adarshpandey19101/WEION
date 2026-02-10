import { ChevronsUpDown, Plus } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

export function OrgSwitcher() {
    const [isOpen, setIsOpen] = useState(false);
    const [activeOrg, setActiveOrg] = useState("Acme Corp");

    const orgs = ["Acme Corp", "Globex Inc", "Soylent Corp"];

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 w-full px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800/50 rounded-md transition-colors"
            >
                <div className="w-6 h-6 rounded bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-xs font-bold text-white">
                    {activeOrg[0]}
                </div>
                <span className="flex-1 text-left truncate">{activeOrg}</span>
                <ChevronsUpDown className="w-4 h-4 text-slate-500" />
            </button>

            {isOpen && (
                <div className="absolute top-full left-0 w-full mt-1 bg-slate-900 border border-slate-800 rounded-md shadow-xl overflow-hidden z-50">
                    <div className="py-1">
                        {orgs.map((org) => (
                            <button
                                key={org}
                                onClick={() => {
                                    setActiveOrg(org);
                                    setIsOpen(false);
                                }}
                                className={cn(
                                    "flex items-center gap-2 w-full px-3 py-2 text-sm text-left transition-colors",
                                    activeOrg === org
                                        ? "bg-slate-800 text-white"
                                        : "text-slate-400 hover:bg-slate-800/50 hover:text-white"
                                )}
                            >
                                {org}
                            </button>
                        ))}
                        <div className="border-t border-slate-800 my-1" />
                        <button className="flex items-center gap-2 w-full px-3 py-2 text-sm text-slate-400 hover:bg-slate-800/50 hover:text-cyan-400 transition-colors">
                            <Plus className="w-4 h-4" />
                            Create Org
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
