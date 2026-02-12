
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { DashboardShell } from "@/components/layout/DashboardShell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Brain, Target, Zap } from "lucide-react";

export default async function DashboardPage() {
    const supabase = await createClient();

    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
        redirect("/login");
    }

    // Fetch Active Missions Count
    const { count: activeMissionsCount } = await supabase
        .from('missions')
        .select('*', { count: 'exact', head: true })
        .eq('status', 'active');

    // Fetch Recent Missions
    const { data: recentMissions } = await supabase
        .from('missions')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(5);

    return (
        <DashboardShell user={user}>
            <div className="space-y-6">
                <h1 className="text-3xl font-bold text-white">Console Overview</h1>

                {/* Stats Grid */}
                <div className="grid md:grid-cols-4 gap-6">
                    <Card className="border-slate-800 bg-slate-900/50">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-slate-400">
                                Active Missions
                            </CardTitle>
                            <Target className="h-4 w-4 text-cyan-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-white">{activeMissionsCount || 0}</div>
                            <p className="text-xs text-slate-500">Live Goals</p>
                        </CardContent>
                    </Card>
                    <Card className="border-slate-800 bg-slate-900/50">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-slate-400">
                                Cognitive Load
                            </CardTitle>
                            <Brain className="h-4 w-4 text-purple-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-white">42%</div>
                            <p className="text-xs text-slate-500">Optimal range</p>
                        </CardContent>
                    </Card>
                    <Card className="border-slate-800 bg-slate-900/50">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-slate-400">
                                Actions Executed
                            </CardTitle>
                            <Zap className="h-4 w-4 text-yellow-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-white">1,240</div>
                            <p className="text-xs text-slate-500">+18% efficiency</p>
                        </CardContent>
                    </Card>
                    <Card className="border-slate-800 bg-slate-900/50">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-slate-400">
                                System Health
                            </CardTitle>
                            <Activity className="h-4 w-4 text-green-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-green-400">99.9%</div>
                            <p className="text-xs text-slate-500">All systems nominal</p>
                        </CardContent>
                    </Card>
                </div>

                {/* Main Content Area */}
                <div className="grid md:grid-cols-3 gap-6">
                    {/* Recent Activity */}
                    <Card className="col-span-2 border-slate-800 bg-slate-900/50">
                        <CardHeader>
                            <CardTitle>Live Execution Stream</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {recentMissions && recentMissions.length > 0 ? (
                                    recentMissions.map((mission: any) => (
                                        <div key={mission.id} className="flex items-start gap-4 p-3 rounded-lg hover:bg-slate-800/50 transition-colors">
                                            <div className="w-2 h-2 mt-2 rounded-full bg-cyan-500 animate-pulse" />
                                            <div>
                                                <p className="text-sm text-slate-300">
                                                    {mission.title}
                                                </p>
                                                <p className="text-xs text-slate-500 mt-1">Status: {mission.status}</p>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="text-sm text-slate-500 p-4 text-center">
                                        No active missions found. Start a new mission in the AI Console.
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    {/* System Alerts */}
                    <Card className="border-slate-800 bg-slate-900/50">
                        <CardHeader>
                            <CardTitle>System Notifications</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div className="p-3 rounded-lg border border-yellow-500/20 bg-yellow-500/10">
                                    <p className="text-sm text-yellow-200">System initialized.</p>
                                </div>
                                <div className="p-3 rounded-lg border border-blue-500/20 bg-blue-500/10">
                                    <p className="text-sm text-blue-200">Database connection established.</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

            </div>
        </DashboardShell>
    );
}
