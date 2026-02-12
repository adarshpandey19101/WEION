"use client";

interface TableRendererProps {
    rows: string[][];
    headers?: string[];
}

export function TableRenderer({ rows, headers }: TableRendererProps) {
    return (
        <div className="my-4 overflow-x-auto rounded-lg border border-slate-700">
            <table className="w-full border-collapse bg-slate-900">
                {headers && headers.length > 0 && (
                    <thead>
                        <tr className="bg-slate-800">
                            {headers.map((header, idx) => (
                                <th
                                    key={idx}
                                    className="px-4 py-3 text-left text-sm font-semibold text-cyan-400 border-b border-slate-700"
                                >
                                    {header}
                                </th>
                            ))}
                        </tr>
                    </thead>
                )}
                <tbody>
                    {rows.map((row, rowIdx) => (
                        <tr
                            key={rowIdx}
                            className="hover:bg-slate-800/50 transition-colors border-b border-slate-800 last:border-0"
                        >
                            {row.map((cell, cellIdx) => (
                                <td
                                    key={cellIdx}
                                    className="px-4 py-3 text-sm text-slate-300 break-words"
                                >
                                    {cell}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
