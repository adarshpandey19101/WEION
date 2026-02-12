"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { User } from "@supabase/supabase-js";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Loader2, Paperclip } from "lucide-react";
import { FileUpload } from "@/components/ai-console/FileUpload";
import { uploadMultipleFiles } from "@/lib/file-upload";

interface MissionDialogProps {
    user: User;
    isOpen: boolean;
    onClose: () => void;
    onSuccess?: () => void;
}

export function MissionDialog({ user, isOpen, onClose, onSuccess }: MissionDialogProps) {
    const supabase = createClient();
    const [isLoading, setIsLoading] = useState(false);
    const [showFileUpload, setShowFileUpload] = useState(false);
    const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        priority: "medium" as "low" | "medium" | "high",
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // Create mission
            const { data: missionData, error } = await supabase
                .from("missions")
                .insert({
                    user_id: user.id,
                    title: formData.title,
                    description: formData.description,
                    priority: formData.priority,
                    status: "active",
                })
                .select()
                .single();

            if (error) throw error;

            // Upload files if any
            if (attachedFiles.length > 0 && missionData) {
                await uploadMultipleFiles(attachedFiles, user.id, {
                    missionId: missionData.id,
                });
            }

            // Reset form
            setFormData({
                title: "",
                description: "",
                priority: "medium",
            });
            setAttachedFiles([]);
            setShowFileUpload(false);

            // Close dialog and trigger success callback
            onClose();
            if (onSuccess) {
                onSuccess();
            }
        } catch (error) {
            console.error("Error creating mission:", error);
            alert("Failed to create mission. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[600px] bg-slate-900 border-slate-800 max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle className="text-white">Create New Mission</DialogTitle>
                    <DialogDescription className="text-slate-400">
                        Define a new autonomous mission for WEION to plan and execute.
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit}>
                    <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                            <Label htmlFor="title" className="text-white">
                                Mission Title
                            </Label>
                            <Input
                                id="title"
                                placeholder="e.g., Market Research Analysis"
                                value={formData.title}
                                onChange={(e) =>
                                    setFormData({ ...formData, title: e.target.value })
                                }
                                className="bg-slate-800 border-slate-700 text-white"
                                required
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="description" className="text-white">
                                Description
                            </Label>
                            <Textarea
                                id="description"
                                placeholder="Describe the mission objectives, expected outcomes, and any specific constraints..."
                                value={formData.description}
                                onChange={(e) =>
                                    setFormData({ ...formData, description: e.target.value })
                                }
                                className="bg-slate-800 border-slate-700 text-white h-24"
                                required
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="priority" className="text-white">
                                Priority Level
                            </Label>
                            <Select
                                value={formData.priority}
                                onValueChange={(value: "low" | "medium" | "high") =>
                                    setFormData({ ...formData, priority: value })
                                }
                            >
                                <SelectTrigger className="bg-slate-800 border-slate-700 text-white">
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent className="bg-slate-800 border-slate-700">
                                    <SelectItem value="low" className="text-white">
                                        Low - Background Processing
                                    </SelectItem>
                                    <SelectItem value="medium" className="text-white">
                                        Medium - Standard Timeline
                                    </SelectItem>
                                    <SelectItem value="high" className="text-white">
                                        High - Urgent Execution
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Optional File Upload */}
                        <div className="grid gap-2">
                            <div className="flex items-center justify-between">
                                <Label className="text-white">Reference Files (Optional)</Label>
                                <Button
                                    type="button"
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => setShowFileUpload(!showFileUpload)}
                                    className="text-cyan-400 hover:text-cyan-300"
                                >
                                    <Paperclip className="w-4 h-4 mr-1" />
                                    {showFileUpload ? "Hide" : "Add Files"}
                                </Button>
                            </div>
                            {showFileUpload && (
                                <div className="mt-2">
                                    <FileUpload
                                        onFilesSelected={setAttachedFiles}
                                        maxFiles={5}
                                        maxSizeMB={50}
                                        allowFolders={false}
                                    />
                                </div>
                            )}
                            {attachedFiles.length > 0 && (
                                <p className="text-xs text-slate-500">
                                    {attachedFiles.length} file(s) attached
                                </p>
                            )}
                        </div>
                    </div>
                    <DialogFooter>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={onClose}
                            className="border-slate-700"
                            disabled={isLoading}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            className="bg-cyan-600 hover:bg-cyan-700"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Creating...
                                </>
                            ) : (
                                "Create Mission"
                            )}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
