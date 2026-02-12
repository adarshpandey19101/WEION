"use client";

import { useState } from "react";
import Image from "next/image";
import { Download, ZoomIn } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ImageRendererProps {
    imageUrl: string;
    caption?: string;
}

export function ImageRenderer({ imageUrl, caption }: ImageRendererProps) {
    const [isZoomed, setIsZoomed] = useState(false);

    const handleDownload = async () => {
        try {
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = caption || "ai-generated-image.png";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("Error downloading image:", error);
        }
    };

    return (
        <div className="my-4 rounded-lg border border-slate-700 overflow-hidden bg-slate-900">
            <div className="relative group">
                <img
                    src={imageUrl}
                    alt={caption || "AI Generated Image"}
                    className="w-full h-auto cursor-pointer hover:opacity-90 transition-opacity"
                    onClick={() => setIsZoomed(!isZoomed)}
                />
                <div className="absolute top-2 right-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                        size="sm"
                        variant="secondary"
                        className="bg-slate-800/90 hover:bg-slate-700"
                        onClick={() => setIsZoomed(!isZoomed)}
                    >
                        <ZoomIn className="w-4 h-4" />
                    </Button>
                    <Button
                        size="sm"
                        variant="secondary"
                        className="bg-slate-800/90 hover:bg-slate-700"
                        onClick={handleDownload}
                    >
                        <Download className="w-4 h-4" />
                    </Button>
                </div>
            </div>
            {caption && (
                <div className="p-3 bg-slate-800 text-sm text-slate-300 border-t border-slate-700">
                    {caption}
                </div>
            )}

            {/* Zoomed Modal */}
            {isZoomed && (
                <div
                    className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
                    onClick={() => setIsZoomed(false)}
                >
                    <img
                        src={imageUrl}
                        alt={caption || "AI Generated Image"}
                        className="max-w-full max-h-full object-contain"
                    />
                </div>
            )}
        </div>
    );
}
