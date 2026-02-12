"use client";

import { useState, useRef } from "react";
import { Play, Pause, Volume2, VolumeX, Maximize, Download } from "lucide-react";
import { Button } from "@/components/ui/button";

interface VideoRendererProps {
    videoUrl: string;
    caption?: string;
    thumbnail?: string;
}

export function VideoRenderer({ videoUrl, caption, thumbnail }: VideoRendererProps) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [isMuted, setIsMuted] = useState(false);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const videoRef = useRef<HTMLVideoElement>(null);

    const togglePlay = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const toggleMute = () => {
        if (videoRef.current) {
            videoRef.current.muted = !isMuted;
            setIsMuted(!isMuted);
        }
    };

    const toggleFullscreen = () => {
        if (videoRef.current) {
            if (!isFullscreen) {
                videoRef.current.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
            setIsFullscreen(!isFullscreen);
        }
    };

    const handleDownload = () => {
        const a = document.createElement("a");
        a.href = videoUrl;
        a.download = caption || "ai-generated-video.mp4";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    return (
        <div className="my-4 rounded-lg border border-slate-700 overflow-hidden bg-slate-900">
            <div className="relative group">
                <video
                    ref={videoRef}
                    src={videoUrl}
                    poster={thumbnail}
                    className="w-full h-auto"
                    onClick={togglePlay}
                    onEnded={() => setIsPlaying(false)}
                >
                    Your browser does not support the video tag.
                </video>

                {/* Video Controls */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="flex items-center gap-2">
                        <Button
                            size="sm"
                            variant="ghost"
                            className="text-white hover:bg-white/20"
                            onClick={togglePlay}
                        >
                            {isPlaying ? (
                                <Pause className="w-4 h-4" />
                            ) : (
                                <Play className="w-4 h-4" />
                            )}
                        </Button>
                        <Button
                            size="sm"
                            variant="ghost"
                            className="text-white hover:bg-white/20"
                            onClick={toggleMute}
                        >
                            {isMuted ? (
                                <VolumeX className="w-4 h-4" />
                            ) : (
                                <Volume2 className="w-4 h-4" />
                            )}
                        </Button>
                        <div className="flex-1" />
                        <Button
                            size="sm"
                            variant="ghost"
                            className="text-white hover:bg-white/20"
                            onClick={handleDownload}
                        >
                            <Download className="w-4 h-4" />
                        </Button>
                        <Button
                            size="sm"
                            variant="ghost"
                            className="text-white hover:bg-white/20"
                            onClick={toggleFullscreen}
                        >
                            <Maximize className="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            </div>
            {caption && (
                <div className="p-3 bg-slate-800 text-sm text-slate-300 border-t border-slate-700">
                    {caption}
                </div>
            )}
        </div>
    );
}
