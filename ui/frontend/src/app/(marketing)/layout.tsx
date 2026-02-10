"use client";

import { PublicHeader } from "@/components/layout/PublicHeader";
import { PublicFooter } from "@/components/layout/PublicFooter";

export default function MarketingLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-background font-sans text-foreground">
            <PublicHeader />
            <main className="pt-16">
                {children}
            </main>
            <PublicFooter />
        </div>
    );
}
