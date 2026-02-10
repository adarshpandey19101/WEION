"use client";

import { Shield, Lock, FileCheck, Server, AlertTriangle, Eye } from "lucide-react";

export default function SecurityPage() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Header */}
            <section className="py-24 px-6 bg-background text-center">
                <div className="max-w-3xl mx-auto space-y-6">
                    <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium text-muted-foreground capitalize">
                        <Shield className="w-3 h-3 mr-2 text-green-500" />
                        Security & Compliance
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
                        Your data. Your infrastructure.<br />Our software.
                    </h1>
                    <p className="text-xl text-muted-foreground leading-relaxed">
                        WEION is architected for zero-trust environments. We process data within your perimeter or in isolated, single-tenant cloud instances.
                    </p>
                </div>
            </section>

            {/* Grid */}
            <section className="py-16 px-6">
                <div className="container mx-auto max-w-5xl">
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {/* Card 1 */}
                        <div className="p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-colors space-y-4">
                            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                                <Lock className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold">SOC 2 Type II</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                We undergo rigorous annual audits by third-party firms to ensure our controls meet the highest industry standards for security, availability, and confidentiality.
                            </p>
                        </div>

                        {/* Card 2 */}
                        <div className="p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-colors space-y-4">
                            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                                <Server className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold">Data Residency</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                Choose where your data lives. We support deployment regions across US, EU, and APAC to help you meet local data sovereignty requirements.
                            </p>
                        </div>

                        {/* Card 3 */}
                        <div className="p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-colors space-y-4">
                            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                                <FileCheck className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold">Encryption at Rest</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                All persistent data is encrypted using AES-256 GCM. Keys are managed via AWS KMS or HashiCorp Vault, with optional BYOK support.
                            </p>
                        </div>

                        {/* Card 4 */}
                        <div className="p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-colors space-y-4">
                            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                                <AlertTriangle className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold">Vulnerability Management</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                Continuous automated scanning of our codebase and infrastructure. We maintain a public bug bounty program to incentivize responsible disclosure.
                            </p>
                        </div>

                        {/* Card 5 */}
                        <div className="p-8 rounded-2xl border bg-card hover:border-foreground/20 transition-colors space-y-4">
                            <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                                <Eye className="w-5 h-5 text-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold">Access transparency</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                See exactly when WEION support staff access your instance. Just-in-time access approvals are logged to your immutable audit trail.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
