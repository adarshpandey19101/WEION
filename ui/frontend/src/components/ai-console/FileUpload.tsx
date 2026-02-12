"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, File, Image, Video, FileText, Music, Archive } from "lucide-react";
import { formatFileSize, validateFile } from "@/lib/file-upload";
import { Button } from "@/components/ui/button";

interface FileUploadProps {
    onFilesSelected: (files: File[]) => void;
    maxFiles?: number;
    maxSizeMB?: number;
    acceptedFileTypes?: string[];
    allowFolders?: boolean;
}

export function FileUpload({
    onFilesSelected,
    maxFiles = 10,
    maxSizeMB = 100,
    acceptedFileTypes,
    allowFolders = true,
}: FileUploadProps) {
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [errors, setErrors] = useState<string[]>([]);

    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            setErrors([]);
            const newErrors: string[] = [];
            const validFiles: File[] = [];

            acceptedFiles.forEach((file) => {
                const validation = validateFile(file, maxSizeMB);
                if (validation.valid) {
                    validFiles.push(file);
                } else {
                    newErrors.push(`${file.name}: ${validation.error}`);
                }
            });

            if (validFiles.length + selectedFiles.length > maxFiles) {
                newErrors.push(`Maximum ${maxFiles} files allowed`);
                return;
            }

            const updatedFiles = [...selectedFiles, ...validFiles];
            setSelectedFiles(updatedFiles);
            setErrors(newErrors);
            onFilesSelected(updatedFiles);
        },
        [selectedFiles, maxFiles, maxSizeMB, onFilesSelected]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        maxFiles,
        accept: acceptedFileTypes
            ? Object.fromEntries(acceptedFileTypes.map((type) => [type, []]))
            : undefined,
    });

    const removeFile = (index: number) => {
        const updatedFiles = selectedFiles.filter((_, i) => i !== index);
        setSelectedFiles(updatedFiles);
        onFilesSelected(updatedFiles);
    };

    const getFileIcon = (file: File) => {
        const type = file.type;
        if (type.startsWith("image/")) return <Image className="w-5 h-5 text-blue-500" />;
        if (type.startsWith("video/")) return <Video className="w-5 h-5 text-purple-500" />;
        if (type.startsWith("audio/")) return <Music className="w-5 h-5 text-green-500" />;
        if (type.includes("pdf") || type.includes("document")) {
            return <FileText className="w-5 h-5 text-red-500" />;
        }
        if (type.includes("zip") || type.includes("rar")) {
            return <Archive className="w-5 h-5 text-yellow-500" />;
        }
        return <File className="w-5 h-5 text-slate-500" />;
    };

    return (
        <div className="w-full space-y-4">
            {/* Dropzone Area */}
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive
                        ? "border-cyan-500 bg-cyan-500/10"
                        : "border-slate-700 hover:border-slate-600 bg-slate-900/50"
                    }`}
            >
                <input {...getInputProps()} />
                <Upload
                    className={`w-12 h-12 mx-auto mb-4 ${isDragActive ? "text-cyan-500" : "text-slate-500"
                        }`}
                />
                <p className="text-white text-sm font-medium mb-1">
                    {isDragActive
                        ? "Drop files here..."
                        : allowFolders
                            ? "Drag & drop files or folders here"
                            : "Drag & drop files here"}
                </p>
                <p className="text-slate-500 text-xs">
                    or click to browse ({maxFiles} files max, {maxSizeMB}MB each)
                </p>
                <p className="text-slate-600 text-xs mt-2">
                    Supports: Images, Documents, Videos, Audio, Archives, and more
                </p>
            </div>

            {/* Error Messages */}
            {errors.length > 0 && (
                <div className="space-y-1">
                    {errors.map((error, index) => (
                        <p key={index} className="text-red-400 text-xs">
                            {error}
                        </p>
                    ))}
                </div>
            )}

            {/* Selected Files List */}
            {selectedFiles.length > 0 && (
                <div className="space-y-2">
                    <p className="text-slate-400 text-sm font-medium">
                        Selected Files ({selectedFiles.length})
                    </p>
                    <div className="space-y-2 max-h-60 overflow-y-auto">
                        {selectedFiles.map((file, index) => (
                            <div
                                key={index}
                                className="flex items-center gap-3 p-3 bg-slate-800 rounded-lg border border-slate-700"
                            >
                                {getFileIcon(file)}
                                <div className="flex-1 min-w-0">
                                    <p className="text-white text-sm truncate">{file.name}</p>
                                    <p className="text-slate-500 text-xs">
                                        {formatFileSize(file.size)}
                                    </p>
                                </div>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-8 w-8 text-slate-400 hover:text-white"
                                    onClick={() => removeFile(index)}
                                >
                                    <X className="w-4 h-4" />
                                </Button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
