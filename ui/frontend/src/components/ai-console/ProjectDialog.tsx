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
import { Loader2 } from "lucide-react";

interface ProjectDialogProps {
    user: User;
    isOpen: boolean;
    onClose: () => void;
    onSuccess?: () => void;
}

const PROJECT_COLORS = [
    "#8b5cf6", // purple
    "#3b82f6", // blue
    "#06b6d4", // cyan
    "#10b981", // green
    "#f59e0b", // amber
    "#ef4444", // red
    "#ec4899", // pink
];

export function ProjectDialog({ user, isOpen, onClose, onSuccess }: ProjectDialogProps) {
    const supabase = createClient();
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: "",
        description: "",
        color: PROJECT_COLORS[0],
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const { error } = await supabase.from("projects").insert({
                user_id: user.id,
                name: formData.name,
                description: formData.description,
                color: formData.color,
            });

            if (error) throw error;

            // Reset form
            setFormData({
                name: "",
                description: "",
                color: PROJECT_COLORS[0],
            });

            onClose();
            if (onSuccess) {
                onSuccess();
            }
        } catch (error) {
            console.error("Error creating project:", error);
            alert("Failed to create project. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px] bg-slate-900 border-slate-800">
                <DialogHeader>
                    <DialogTitle className="text-white">Create New Project</DialogTitle>
                    <DialogDescription className="text-slate-400">
                        Organize your chats into project folders.
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit}>
                    <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                            <Label htmlFor="name" className="text-white">
                                Project Name
                            </Label>
                            <Input
                                id="name"
                                placeholder="e.g., Client Work, Personal Projects"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="bg-slate-800 border-slate-700 text-white"
                                required
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="description" className="text-white">
                                Description (Optional)
                            </Label>
                            <Textarea
                                id="description"
                                placeholder="Brief description of this project..."
                                value={formData.description}
                                onChange={(e) =>
                                    setFormData({ ...formData, description: e.target.value })
                                }
                                className="bg-slate-800 border-slate-700 text-white h-20"
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label className="text-white">Folder Color</Label>
                            <div className="flex gap-2">
                                {PROJECT_COLORS.map((color) => (
                                    <button
                                        key={color}
                                        type="button"
                                        onClick={() => setFormData({ ...formData, color })}
                                        className={`w-8 h-8 rounded-full border-2 transition-all ${formData.color === color
                                                ? "border-white scale-110"
                                                : "border-transparent hover:scale-105"
                                            }`}
                                        style={{ backgroundColor: color }}
                                    />
                                ))}
                            </div>
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
                            className="bg-purple-600 hover:bg-purple-700"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Creating...
                                </>
                            ) : (
                                "Create Project"
                            )}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
