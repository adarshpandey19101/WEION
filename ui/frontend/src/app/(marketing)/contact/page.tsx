"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Mail, MessageSquare, MapPin } from "lucide-react";

export default function ContactPage() {
    return (
        <div className="flex flex-col min-h-screen py-24 bg-background">
            <div className="container mx-auto px-6 max-w-5xl">
                <div className="grid md:grid-cols-2 gap-12 lg:gap-24">
                    {/* Left Column: Info */}
                    <div className="space-y-8">
                        <div>
                            <h1 className="text-4xl font-bold tracking-tight mb-4">Contact Sales</h1>
                            <p className="text-lg text-muted-foreground">
                                Ready to deploy autonomous agents? Our team is here to help you scope your pilot and define your governance model.
                            </p>
                        </div>

                        <div className="space-y-6">
                            <div className="flex items-start gap-4">
                                <Mail className="w-6 h-6 text-muted-foreground mt-1" />
                                <div>
                                    <h3 className="font-medium">Email</h3>
                                    <p className="text-sm text-muted-foreground">enterprise@weion.ai</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-4">
                                <MessageSquare className="w-6 h-6 text-muted-foreground mt-1" />
                                <div>
                                    <h3 className="font-medium">Support</h3>
                                    <p className="text-sm text-muted-foreground">help.weion.ai</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-4">
                                <MapPin className="w-6 h-6 text-muted-foreground mt-1" />
                                <div>
                                    <h3 className="font-medium">Headquarters</h3>
                                    <p className="text-sm text-muted-foreground">
                                        415 Mission Street<br />
                                        San Francisco, CA 94105
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Form */}
                    <div>
                        <Card className="border-border shadow-sm">
                            <CardHeader>
                                <CardTitle>Send us a message</CardTitle>
                                <CardDescription>We usually respond within 24 hours.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <label htmlFor="first-name" className="text-sm font-medium">First name</label>
                                        <Input id="first-name" placeholder="Jane" />
                                    </div>
                                    <div className="space-y-2">
                                        <label htmlFor="last-name" className="text-sm font-medium">Last name</label>
                                        <Input id="last-name" placeholder="Doe" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="email" className="text-sm font-medium">Work Email</label>
                                    <Input id="email" type="email" placeholder="jane@company.com" />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="message" className="text-sm font-medium">Message</label>
                                    <textarea
                                        id="message"
                                        className="flex min-h-[120px] w-full rounded-md border border-input bg-zinc-900/50 px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                                        placeholder="Tell us about your use case..."
                                    />
                                </div>
                                <Button className="w-full">
                                    Send Message
                                </Button>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
