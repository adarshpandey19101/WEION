"use client";

import {
    LineChart,
    Line,
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

interface ChartRendererProps {
    data: any;
    type?: "line" | "bar" | "pie";
}

const COLORS = ["#06b6d4", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#ec4899"];

export function ChartRenderer({ data, type = "line" }: ChartRendererProps) {
    if (!data || !data.data) {
        return (
            <div className="text-red-400 text-sm p-4 bg-red-950 rounded border border-red-800">
                Invalid chart data format
            </div>
        );
    }

    const chartData = data.data.datasets?.[0]?.data || [];
    const labels = data.data.labels || [];
    const datasetLabel = data.data.datasets?.[0]?.label || "Data";

    const formattedData = labels.map((label: string, index: number) => ({
        name: label,
        value: chartData[index],
    }));

    return (
        <div className="my-4 p-6 bg-slate-900 rounded-lg border border-slate-700">
            <ResponsiveContainer width="100%" height={300}>
                {type === "line" ? (
                    <LineChart data={formattedData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="name" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#1e293b",
                                border: "1px solid #475569",
                                borderRadius: "8px",
                            }}
                        />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#06b6d4"
                            strokeWidth={2}
                            dot={{ fill: "#06b6d4" }}
                            name={datasetLabel}
                        />
                    </LineChart>
                ) : type === "bar" ? (
                    <BarChart data={formattedData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="name" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#1e293b",
                                border: "1px solid #475569",
                                borderRadius: "8px",
                            }}
                        />
                        <Legend />
                        <Bar dataKey="value" fill="#8b5cf6" name={datasetLabel} />
                    </BarChart>
                ) : (
                    <PieChart>
                        <Pie
                            data={formattedData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) =>
                                `${name}: ${((percent || 0) * 100).toFixed(0)}%`
                            }
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="value"
                        >
                            {formattedData.map((entry: any, index: number) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#1e293b",
                                border: "1px solid #475569",
                                borderRadius: "8px",
                            }}
                        />
                    </PieChart>
                )}
            </ResponsiveContainer>
        </div>
    );
}
