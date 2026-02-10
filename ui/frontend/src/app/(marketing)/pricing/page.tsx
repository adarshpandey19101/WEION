"use client";

import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

const plans = [
    {
        name: "Free",
        price: "$0",
        period: "/month",
        description: "For individuals exploring autonomous agents.",
        features: ["5 Missions / day", "Basic Reasoning Model", "Community Support", "1 Project"],
        button: "Get Started",
        href: "/signup",
        popular: false
    },
    {
        name: "Pro",
        price: "$49",
        period: "/month",
        description: "For professionals needing a dedicated executive assistant.",
        features: ["Unlimited Missions", "Advanced Reasoning (GPT-4o)", "Priority Support", "5 Projects", "Web Browsing Capability"],
        button: "Start Trial",
        href: "/signup",
        popular: true
    },
    {
        name: "Organization",
        price: "$199",
        period: "/seat/month",
        description: "For teams collaborating on complex workflows.",
        features: ["Shared Team Memory", "Role-Based Access Control", "API Access", "Unlimited Projects", "Custom Tool Integrations"],
        button: "Contact Sales",
        href: "/contact",
        popular: false
    }
];

export default function PricingPage() {
    return (
        <div className="flex flex-col min-h-screen py-24 bg-background">
            <div className="container mx-auto px-6 max-w-6xl">
                <div className="text-center mb-20 space-y-4">
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Simple, transparent pricing.</h1>
                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                        Start free, upgrade as you scale. No hidden fees or surprise overages.
                    </p>
                </div>

                <div className="grid lg:grid-cols-3 gap-8">
                    {plans.map((plan) => (
                        <div
                            key={plan.name}
                            className={cn(
                                "flex flex-col p-8 rounded-2xl border bg-card transition-all duration-300",
                                plan.popular ? "border-primary ring-1 ring-primary shadow-lg scale-105 z-10" : "border-border hover:border-foreground/20"
                            )}
                        >
                            <div className="mb-6">
                                <h3 className="text-lg font-medium">{plan.name}</h3>
                                <div className="mt-4 flex items-baseline text-4xl font-bold tracking-tight">
                                    {plan.price}
                                    <span className="text-base font-normal text-muted-foreground ml-1">{plan.period}</span>
                                </div>
                                <p className="mt-4 text-sm text-muted-foreground">{plan.description}</p>
                            </div>

                            <ul className="flex-1 space-y-4 mb-8">
                                {plan.features.map((feature) => (
                                    <li key={feature} className="flex items-center text-sm">
                                        <Check className="w-4 h-4 mr-3 text-primary" />
                                        {feature}
                                    </li>
                                ))}
                            </ul>

                            <Button
                                variant={plan.popular ? "default" : "outline"}
                                className="w-full"
                                asChild
                            >
                                <Link href={plan.href}>{plan.button}</Link>
                            </Button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
