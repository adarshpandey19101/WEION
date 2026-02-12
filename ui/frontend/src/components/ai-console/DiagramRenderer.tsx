"use client";

import mermaid from "mermaid";
import { useEffect, useRef } from "react";

interface DiagramRendererProps {
    code: string;
}

export function DiagramRenderer({ code }: DiagramRendererProps) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (containerRef.current) {
            mermaid.initialize({
                startOnLoad: true,
                theme: "dark",
                themeVariables: {
                    primaryColor: "#06b6d4",
                    primaryTextColor: "#fff",
                    primaryBorderColor: "#0891b2",
                    lineColor: "#64748b",
                    secondaryColor: "#8b5cf6",
                    tertiaryColor: "#10b981",
                },
            });

            const renderDiagram = async () => {
                try {
                    const { svg } = await mermaid.render("mermaid-diagram", code);
                    if (containerRef.current) {
                        containerRef.current.innerHTML = svg;
                    }
                } catch (error) {
                    console.error("Mermaid rendering error:", error);
                    if (containerRef.current) {
                        containerRef.current.innerHTML = `
                            <div class="text-red-400 text-sm p-4 bg-red-950 rounded border border-red-800">
                                Failed to render diagram. Please check the syntax.
                            </div>
                        `;
                    }
                }
            };

            renderDiagram();
        }
    }, [code]);

    return (
        <div className="my-4 p-4 bg-slate-900 rounded-lg border border-slate-700">
            <div ref={containerRef} className="mermaid-container" />
        </div>
    );
}
