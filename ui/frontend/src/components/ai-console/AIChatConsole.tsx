"use client";

import { useState, useEffect, useRef } from "react";
import { createClient } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { Send, Paperclip, Mic, Bot, User as UserIcon, Loader2, MicOff, X, Download, File as FileIcon } from "lucide-react";
import { User } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { generateEnhancedResponse, ThinkingStep } from "@/lib/response-formatter";
import { useSpeechRecognition } from "@/hooks/use-speech-recognition";
import { uploadMultipleFiles, formatFileSize, getFileDownloadUrl } from "@/lib/file-upload";
import { FileUpload } from "@/components/ai-console/FileUpload";
import { ImageRenderer } from "@/components/ai-console/ImageRenderer";
import { VideoRenderer } from "@/components/ai-console/VideoRenderer";
import { DiagramRenderer } from "@/components/ai-console/DiagramRenderer";
import { ChartRenderer } from "@/components/ai-console/ChartRenderer";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

interface Message {
    id: string;
    role: "user" | "ai";
    content: string;
    created_at: string;
    files?: AttachedFile[];
}

interface AttachedFile {
    id: string;
    filename: string;
    file_size: number;
    storage_path: string;
    mime_type: string;
}

interface AIChatConsoleProps {
    user: User;
    chatId: string | null;
    onChatCreated?: (chatId: string) => void;
}

export function AIChatConsole({ user, chatId, onChatCreated }: AIChatConsoleProps) {
    const supabase = createClient();
    const router = useRouter();
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [currentChatId, setCurrentChatId] = useState<string | null>(chatId);
    const [thinkingSteps, setThinkingSteps] = useState<ThinkingStep[]>([]);
    const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
    const [showFileDialog, setShowFileDialog] = useState(false);
    const [uploadingFiles, setUploadingFiles] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Voice input
    const { isListening, transcript, startListening, stopListening, isSupported } = useSpeechRecognition();

    // Initial system message
    const systemMessage: Message = {
        id: "system-welcome",
        role: "ai",
        content: "Systems online. All cognitive modules are active. I am ready to plan and execute complex missions. What is our objective today?",
        created_at: new Date().toISOString(),
    };

    // Update input when transcript changes
    useEffect(() => {
        if (transcript) {
            setInput(transcript);
        }
    }, [transcript]);

    // Auto-send when user stops speaking
    useEffect(() => {
        if (!isListening && transcript.trim()) {
            const timer = setTimeout(() => {
                handleSendMessage();
            }, 1000);
            return () => clearTimeout(timer);
        }
    }, [isListening, transcript]);

    // Load messages when chatId changes
    useEffect(() => {
        if (chatId) {
            loadChatMessages(chatId);
            setCurrentChatId(chatId);
        } else {
            // New chat - reset to system message
            setMessages([systemMessage]);
            setCurrentChatId(null);
        }
    }, [chatId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, thinkingSteps]);

    const loadChatMessages = async (chatIdToLoad: string) => {
        try {
            // Load messages
            const { data: messagesData, error: messagesError } = await supabase
                .from("messages")
                .select("*")
                .eq("chat_id", chatIdToLoad)
                .order("created_at", { ascending: true });

            if (messagesError) throw messagesError;

            // Load files for each message
            const messagesWithFiles = await Promise.all(
                messagesData.map(async (msg) => {
                    const { data: filesData } = await supabase
                        .from("files")
                        .select("*")
                        .eq("chat_id", chatIdToLoad)
                        .eq("message_id", msg.id);

                    return {
                        ...msg,
                        files: filesData || [],
                    };
                })
            );

            setMessages(messagesWithFiles || []);
        } catch (error) {
            console.error("Error loading messages:", error);
        }
    };

    const handleSendMessage = async () => {
        const userMessageContent = input.trim();
        if (!userMessageContent && attachedFiles.length === 0) return;

        setIsLoading(true);
        setInput("");

        try {
            let activeChatId = currentChatId;

            // Create new chat if needed
            if (!activeChatId) {
                const { data: chatData, error: chatError } = await supabase
                    .from("chats")
                    .insert({
                        user_id: user.id,
                        title: userMessageContent.slice(0, 50) || "New Chat",
                    })
                    .select()
                    .single();

                if (chatError) throw chatError;
                activeChatId = chatData.id;
                setCurrentChatId(activeChatId);
                if (activeChatId) {
                    onChatCreated?.(activeChatId);
                }
            }

            // Add user message to UI immediately
            const tempUserMessage: Message = {
                id: `temp-${Date.now()}`,
                role: "user",
                content: userMessageContent,
                created_at: new Date().toISOString(),
                files: [],
            };
            setMessages((prev) => [...prev, tempUserMessage]);

            // Upload files if any
            let uploadedFiles: AttachedFile[] = [];
            if (attachedFiles.length > 0 && activeChatId) {
                setUploadingFiles(true);
                const uploadResults = await uploadMultipleFiles(attachedFiles, user.id, {
                    chatId: activeChatId,
                });
                uploadedFiles = uploadResults
                    .filter((r) => r.success)
                    .map((r) => ({
                        id: r.fileId!,
                        filename: attachedFiles[0].name,
                        file_size: attachedFiles[0].size,
                        storage_path: r.storagePath!,
                        mime_type: attachedFiles[0].type,
                    }));
                setUploadingFiles(false);
                setAttachedFiles([]);
            }

            // Insert user message to database
            const { data: userMessageData, error: userMsgError } = await supabase
                .from("messages")
                .insert({
                    chat_id: activeChatId,
                    role: "user",
                    content: userMessageContent,
                })
                .select()
                .single();

            if (userMsgError) throw userMsgError;

            // Generate Enhanced AI Response
            const { thinkingSteps: steps, response: aiResponseContent } =
                generateEnhancedResponse(userMessageContent);
            setThinkingSteps(steps);

            // Simulate processing time for each step
            for (let i = 0; i < steps.length; i++) {
                await new Promise((resolve) => setTimeout(resolve, 400));
                setThinkingSteps((prev) =>
                    prev.map((step, idx) => (idx === i ? { ...step, status: "complete" } : step))
                );
            }

            // Clear thinking steps
            setThinkingSteps([]);

            // Insert AI message
            const { data: aiMessageData, error: aiMsgError } = await supabase
                .from("messages")
                .insert({
                    chat_id: activeChatId,
                    role: "ai",
                    content: aiResponseContent,
                })
                .select()
                .single();

            if (aiMsgError) throw aiMsgError;

            // Update messages with actual data
            setMessages((prev) => [
                ...prev.filter((m) => m.id !== tempUserMessage.id),
                { ...userMessageData, files: uploadedFiles },
                aiMessageData,
            ]);
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const toggleVoiceInput = () => {
        if (isListening) {
            stopListening();
        } else {
            startListening();
        }
    };

    const handleFileDownload = async (file: AttachedFile) => {
        const url = await getFileDownloadUrl(file.storage_path);
        if (url) {
            window.open(url, "_blank");
        }
    };

    return (
        <div className="flex flex-col h-full bg-slate-950">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((msg, index) => (
                    <div key={`${msg.id}-${msg.created_at || index}`} className="flex gap-4 max-w-3xl mx-auto">
                        <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === "ai" ? "bg-cyan-500/20" : "bg-slate-700"
                                }`}
                        >
                            {msg.role === "ai" ? (
                                <Bot className="w-5 h-5 text-cyan-500" />
                            ) : (
                                <UserIcon className="w-5 h-5 text-slate-300" />
                            )}
                        </div>
                        <div className="flex-1">
                            <div className="text-sm font-bold text-slate-300 mb-1">
                                {msg.role === "ai" ? "WEION Core" : "You"}
                            </div>
                            <div className="text-sm text-slate-300">
                                {msg.role === "ai" ? (
                                    <div className="prose prose-sm prose-invert max-w-none">
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm]}
                                            components={{
                                                img: ({ node, ...props }) => {
                                                    // Check if it's a video or placeholder
                                                    if (props.alt === "video") return null;
                                                    const imgSrc = typeof props.src === 'string' ? props.src : '';
                                                    return (
                                                        <ImageRenderer
                                                            imageUrl={imgSrc || ""}
                                                            caption={props.alt}
                                                        />
                                                    );
                                                },
                                                code({ node, className, children, ...props }: any) {
                                                    const match = /language-(\w+)/.exec(className || "");
                                                    const language = match ? match[1] : "";
                                                    const code = String(children).replace(/\n$/, "");
                                                    const inline = props.inline;

                                                    // Mermaid diagrams
                                                    if (language === "mermaid") {
                                                        return <DiagramRenderer code={code} />;
                                                    }

                                                    // Chart data
                                                    if (language === "chart") {
                                                        try {
                                                            const chartData = JSON.parse(code);
                                                            return (
                                                                <ChartRenderer
                                                                    data={chartData}
                                                                    type={chartData.type || "line"}
                                                                />
                                                            );
                                                        } catch (e) {
                                                            return (
                                                                <div className="text-red-500 text-sm">
                                                                    Invalid chart data
                                                                </div>
                                                            );
                                                        }
                                                    }

                                                    // Video blocks
                                                    if (language === "video") {
                                                        try {
                                                            const videoData = JSON.parse(code);
                                                            return (
                                                                <VideoRenderer
                                                                    videoUrl={videoData.url}
                                                                    caption={videoData.caption}
                                                                    thumbnail={videoData.thumbnail}
                                                                />
                                                            );
                                                        } catch (e) {
                                                            return (
                                                                <div className="text-red-500 text-sm">
                                                                    Invalid video data
                                                                </div>
                                                            );
                                                        }
                                                    }

                                                    // Regular code blocks
                                                    return !inline ? (
                                                        <div className="my-4 rounded-lg overflow-hidden">
                                                            <div className="bg-slate-800 px-4 py-2 text-xs text-slate-400 border-b border-slate-700">
                                                                {language || "code"}
                                                            </div>
                                                            <pre className="bg-slate-900 p-4 overflow-x-auto">
                                                                <code className={className} {...props}>
                                                                    {children}
                                                                </code>
                                                            </pre>
                                                        </div>
                                                    ) : (
                                                        <code
                                                            className="bg-slate-800 px-1.5 py-0.5 rounded text-sm"
                                                            {...props}
                                                        >
                                                            {children}
                                                        </code>
                                                    );
                                                },
                                                table: ({ children }) => (
                                                    <div className="my-4 overflow-x-auto rounded-lg border border-slate-700">
                                                        <table className="w-full border-collapse bg-slate-900">
                                                            {children}
                                                        </table>
                                                    </div>
                                                ),
                                                thead: ({ children }) => (
                                                    <thead className="bg-slate-800">{children}</thead>
                                                ),
                                                th: ({ children }) => (
                                                    <th className="px-4 py-3 text-left text-sm font-semibold text-cyan-400 border-b border-slate-700">
                                                        {children}
                                                    </th>
                                                ),
                                                tr: ({ children }) => (
                                                    <tr className="hover:bg-slate-800/50 transition-colors border-b border-slate-800 last:border-0">
                                                        {children}
                                                    </tr>
                                                ),
                                                td: ({ children }) => (
                                                    <td className="px-4 py-3 text-sm text-slate-300 break-words">
                                                        {children}
                                                    </td>
                                                ),
                                            }}
                                        >
                                            {msg.content}
                                        </ReactMarkdown>
                                    </div>
                                ) : (
                                    msg.content
                                )}

                                {/* Display attached files */}
                                {msg.files && msg.files.length > 0 && (
                                    <div className="mt-3 space-y-2">
                                        {msg.files.map((file) => (
                                            <div
                                                key={file.id}
                                                className="flex items-center gap-2 p-2 bg-slate-800 rounded border border-slate-700 text-xs"
                                            >
                                                <FileIcon className="w-4 h-4 text-slate-400" />
                                                <span className="flex-1 truncate">{file.filename}</span>
                                                <span className="text-slate-500">
                                                    {formatFileSize(file.file_size)}
                                                </span>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-6 w-6"
                                                    onClick={() => handleFileDownload(file)}
                                                >
                                                    <Download className="w-3 h-3" />
                                                </Button>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}

                {/* Thinking animation */}
                {isLoading && thinkingSteps.length > 0 && (
                    <div className="flex gap-4 max-w-3xl mx-auto">
                        <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center shrink-0">
                            <Bot className="w-5 h-5 text-cyan-500 animate-pulse" />
                        </div>
                        <div className="space-y-3 w-full">
                            <div className="text-sm font-bold text-cyan-400">WEION Core</div>
                            <div className="border-l-2 border-slate-700 pl-4 py-1 space-y-2">
                                {thinkingSteps.map((step, idx) => (
                                    <div key={idx} className="flex items-center gap-2 text-xs text-slate-500">
                                        <span
                                            className={`w-1.5 h-1.5 rounded-full bg-${step.color}-500 ${step.status === "processing" ? "animate-pulse" : ""
                                                }`}
                                        />
                                        {step.step}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-slate-900 border-t border-slate-800">
                {/* Attached Files Preview */}
                {attachedFiles.length > 0 && (
                    <div className="max-w-3xl mx-auto mb-2 flex flex-wrap gap-2">
                        {attachedFiles.map((file, idx) => (
                            <div
                                key={idx}
                                className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 rounded-lg border border-slate-700 text-xs"
                            >
                                <FileIcon className="w-3 h-3 text-slate-400" />
                                <span className="text-white">{file.name}</span>
                                <span className="text-slate-500">{formatFileSize(file.size)}</span>
                                <button
                                    onClick={() => setAttachedFiles((prev) => prev.filter((_, i) => i !== idx))}
                                    className="text-slate-400 hover:text-white"
                                >
                                    <X className="w-3 h-3" />
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                <div className="max-w-3xl mx-auto relative">
                    <div className="absolute left-2 bottom-2.5 flex gap-1">
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 text-slate-400 hover:text-white"
                            onClick={() => setShowFileDialog(true)}
                        >
                            <Paperclip className="w-4 h-4" />
                        </Button>
                    </div>
                    <div className="absolute right-2 bottom-2.5 flex gap-1">
                        {isSupported && (
                            <Button
                                variant="ghost"
                                size="icon"
                                className={`h-8 w-8 ${isListening
                                    ? "text-red-500 animate-pulse"
                                    : "text-slate-400 hover:text-white"
                                    }`}
                                onClick={toggleVoiceInput}
                            >
                                {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                            </Button>
                        )}
                        <Button
                            size="icon"
                            className="h-8 w-8 bg-cyan-600 hover:bg-cyan-700 text-white"
                            onClick={handleSendMessage}
                            disabled={isLoading || (!input.trim() && attachedFiles.length === 0)}
                        >
                            {uploadingFiles ? (
                                <Loader2 className="w-3 h-3 animate-spin" />
                            ) : (
                                <Send className="w-3 h-3" />
                            )}
                        </Button>
                    </div>
                    <textarea
                        className="w-full bg-slate-800 border-none rounded-xl py-3 pl-12 pr-24 text-sm text-white placeholder-slate-500 focus:ring-2 focus:ring-cyan-500/50 outline-none resize-none min-h-[50px] max-h-[200px]"
                        placeholder={
                            isListening
                                ? "Listening..."
                                : attachedFiles.length > 0
                                    ? "Add a message (optional)..."
                                    : "Ask me to plan or execute a mission..."
                        }
                        rows={1}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                </div>
                <div className="text-center mt-2 text-[10px] text-slate-600">
                    WEION can make mistakes. Please verify critical autonomous actions.
                </div>
            </div>

            {/* File Upload Dialog */}
            <Dialog open={showFileDialog} onOpenChange={setShowFileDialog}>
                <DialogContent className="bg-slate-900 border-slate-700 max-w-2xl">
                    <DialogHeader>
                        <DialogTitle className="text-white">Upload Files</DialogTitle>
                    </DialogHeader>
                    <FileUpload
                        onFilesSelected={(files) => {
                            setAttachedFiles((prev) => [...prev, ...files]);
                            setShowFileDialog(false);
                        }}
                        maxFiles={10}
                        maxSizeMB={100}
                        allowFolders={true}
                    />
                </DialogContent>
            </Dialog>
        </div>
    );
}
