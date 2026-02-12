import { createClient } from "@/lib/supabase/client";

export interface FileUploadResult {
    success: boolean;
    fileId?: string;
    storagePath?: string;
    error?: string;
}

export interface FileMetadata {
    filename: string;
    fileType: string;
    fileSize: number;
    mimeType: string;
    chatId?: string;
    missionId?: string;
}

/**
 * Determine file type category from MIME type
 */
export function getFileType(mimeType: string): string {
    if (mimeType.startsWith("image/")) return "image";
    if (mimeType.startsWith("video/")) return "video";
    if (mimeType.startsWith("audio/")) return "audio";
    if (mimeType.includes("pdf") || mimeType.includes("document") || mimeType.includes("text")) {
        return "document";
    }
    if (mimeType.includes("zip") || mimeType.includes("rar") || mimeType.includes("7z")) {
        return "archive";
    }
    return "other";
}

/**
 * Format file size for display
 */
export function formatFileSize(bytes: number): string {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

/**
 * Upload file to Supabase Storage and create database record
 */
export async function uploadFile(
    file: File,
    userId: string,
    metadata: Partial<FileMetadata>
): Promise<FileUploadResult> {
    try {
        const supabase = createClient();

        // Generate unique file name
        const timestamp = Date.now();
        const sanitizedFilename = file.name.replace(/[^a-zA-Z0-9.-]/g, "_");
        const storagePath = `${userId}/${timestamp}_${sanitizedFilename}`;

        // Upload to Supabase Storage
        const { data: storageData, error: storageError } = await supabase.storage
            .from("chat-files")
            .upload(storagePath, file, {
                cacheControl: "3600",
                upsert: false,
            });

        if (storageError) {
            console.error("Storage upload error:", storageError);
            return { success: false, error: storageError.message };
        }

        // Create database record
        const fileType = getFileType(file.type);
        const { data: fileRecord, error: dbError } = await supabase
            .from("files")
            .insert({
                user_id: userId,
                chat_id: metadata.chatId || null,
                mission_id: metadata.missionId || null,
                filename: file.name,
                file_type: fileType,
                file_size: file.size,
                storage_path: storagePath,
                mime_type: file.type,
            })
            .select()
            .single();

        if (dbError) {
            console.error("Database insert error:", dbError);
            // Cleanup: delete uploaded file if DB insert fails
            await supabase.storage.from("chat-files").remove([storagePath]);
            return { success: false, error: dbError.message };
        }

        return {
            success: true,
            fileId: fileRecord.id,
            storagePath: storagePath,
        };
    } catch (error: any) {
        console.error("File upload error:", error);
        return { success: false, error: error.message };
    }
}

/**
 * Upload multiple files
 */
export async function uploadMultipleFiles(
    files: File[],
    userId: string,
    metadata: Partial<FileMetadata>
): Promise<FileUploadResult[]> {
    const results = await Promise.all(
        files.map((file) => uploadFile(file, userId, metadata))
    );
    return results;
}

/**
 * Get download URL for a file
 */
export async function getFileDownloadUrl(storagePath: string): Promise<string | null> {
    try {
        const supabase = createClient();
        const { data } = supabase.storage
            .from("chat-files")
            .getPublicUrl(storagePath);

        return data.publicUrl;
    } catch (error) {
        console.error("Error getting download URL:", error);
        return null;
    }
}

/**
 * Delete file from storage and database
 */
export async function deleteFile(fileId: string, storagePath: string): Promise<boolean> {
    try {
        const supabase = createClient();

        // Delete from storage
        const { error: storageError } = await supabase.storage
            .from("chat-files")
            .remove([storagePath]);

        if (storageError) {
            console.error("Storage deletion error:", storageError);
        }

        // Delete from database
        const { error: dbError } = await supabase
            .from("files")
            .delete()
            .eq("id", fileId);

        if (dbError) {
            console.error("Database deletion error:", dbError);
            return false;
        }

        return true;
    } catch (error) {
        console.error("File deletion error:", error);
        return false;
    }
}

/**
 * Validate file before upload
 */
export function validateFile(file: File, maxSizeMB: number = 100): { valid: boolean; error?: string } {
    const maxSize = maxSizeMB * 1024 * 1024; // Convert to bytes

    if (file.size > maxSize) {
        return {
            valid: false,
            error: `File size exceeds ${maxSizeMB}MB limit`,
        };
    }

    // Add more validation as needed
    return { valid: true };
}
