"use client"

import { Check, HelpCircle, Minus } from "lucide-react"
import { useState } from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface PlanFeature {
  name: string
  included: boolean | "partial" | "unlimited"
  tooltip?: string
}

interface PricingPlan {
  name: string
  description: string
  price: {
    monthly: number
    yearly: number
  }
  features: PlanFeature[]
  cta: string
  popular?: boolean
}

const plans: PricingPlan[] = [
  {
    name: "Free",
    description: "Essential features for individuals and small teams",
    price: {
      monthly: 0,
      yearly: 0,
    },
    features: [
      { name: "Up to 3 projects", included: true },
      { name: "Up to 5 team members", included: true },
      { name: "2GB storage", included: true },
      { name: "API access", included: false },
      { name: "Priority support", included: false },
      { name: "Custom domain", included: false },
      { name: "Analytics", included: "partial", tooltip: "Basic analytics only" },
      { name: "Export options", included: "partial", tooltip: "Limited to CSV exports" },
    ],
    cta: "Get Started",
  },
  {
    name: "Pro",
    description: "Perfect for growing teams and businesses",
    price: {
      monthly: 15,
      yearly: 144,
    },
    features: [
      { name: "Up to 15 projects", included: true },
      { name: "Up to 20 team members", included: true },
      { name: "20GB storage", included: true },
      { name: "API access", included: true },
      { name: "Priority support", included: true },
      { name: "Custom domain", included: true },
      { name: "Analytics", included: true },
      { name: "Export options", included: true },
    ],
    cta: "Start Free Trial",
    popular: true,
  },
  {
    name: "Enterprise",
    description: "Advanced features for large organizations",
    price: {
      monthly: 49,
      yearly: 480,
    },
    features: [
      { name: "Unlimited projects", included: "unlimited" },
      { name: "Unlimited team members", included: "unlimited" },
      { name: "100GB storage", included: true },
      { name: "API access", included: true },
      { name: "Priority support", included: true },
      { name: "Custom domain", included: true },
      { name: "Analytics", included: true },
      { name: "Export options", included: true },
    ],
    cta: "Contact Sales",
  },
]

export default function PricingPlans() {
  const [billingCycle, setBillingCycle] = useState<"monthly" | "yearly">("monthly")

  const renderFeatureIcon = (included: boolean | "partial" | "unlimited") => {
    if (included === true) {
      return <Check className="h-5 w-5 text-emerald-500" />
    } else if (included === "partial") {
      return <Minus className="h-5 w-5 text-amber-500" />
    } else if (included === "unlimited") {
      return <span className="text-xs font-medium text-emerald-500">Unlimited</span>
    } else {
      return <Minus className="h-5 w-5 text-muted-foreground opacity-50" />
    }
  }

  return (
    <div className="container mx-auto px-4 py-16">
      <div className="mx-auto mb-16 max-w-2xl text-center">
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">Simple, transparent pricing</h1>
        <p className="text-xl text-muted-foreground">
          Choose the plan that's right for you and start building amazing projects
        </p>
      </div>

      <div className="mb-8 flex items-center justify-center gap-4">
        <span className={`text-sm ${billingCycle === "monthly" ? "font-medium" : "text-muted-foreground"}`}>
          Monthly
        </span>
        <Switch
          checked={billingCycle === "yearly"}
          onCheckedChange={(checked) => setBillingCycle(checked ? "yearly" : "monthly")}
        />
        <div className="flex items-center gap-1.5">
          <span className={`text-sm ${billingCycle === "yearly" ? "font-medium" : "text-muted-foreground"}`}>
            Yearly
          </span>
          <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-800">Save 20%</span>
        </div>
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        <TooltipProvider>
          {plans.map((plan) => (
            <Card
              key={plan.name}
              className={`relative flex flex-col ${
                plan.popular ? "border-emerald-500 shadow-lg shadow-emerald-100/50" : ""
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-0 right-0 mx-auto w-fit rounded-full bg-emerald-500 px-3 py-1 text-xs font-medium text-white">
                  Most Popular
                </div>
              )}
              <CardHeader>
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <CardDescription className="min-h-12">{plan.description}</CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="mb-6">
                  <div className="flex items-baseline">
                    <span className="text-4xl font-bold">
                      ${billingCycle === "monthly" ? plan.price.monthly : Math.round(plan.price.yearly / 12)}
                    </span>
                    <span className="text-muted-foreground">/month</span>
                  </div>
                  {billingCycle === "yearly" && (
                    <p className="text-sm text-muted-foreground">${plan.price.yearly} billed annually</p>
                  )}
                </div>

                <ul className="space-y-3">
                  {plan.features.map((feature) => (
                    <li key={feature.name} className="flex items-center gap-3">
                      <div className="flex h-5 w-5 items-center justify-center">
                        {renderFeatureIcon(feature.included)}
                      </div>
                      <span className="text-sm">
                        {feature.name}
                        {feature.tooltip && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <HelpCircle className="ml-1 inline h-3.5 w-3.5 cursor-help text-muted-foreground" />
                            </TooltipTrigger>
                            <TooltipContent side="top" className="max-w-xs">
                              {feature.tooltip}
                            </TooltipContent>
                          </Tooltip>
                        )}
                      </span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <Button
                  className={`w-full ${
                    plan.popular
                      ? "bg-emerald-500 hover:bg-emerald-600"
                      : plan.name === "Enterprise"
                        ? "bg-slate-800 hover:bg-slate-900"
                        : ""
                  }`}
                >
                  {plan.cta}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </TooltipProvider>
      </div>

      <div className="mt-16 text-center">
        <p className="text-muted-foreground">
          Need a custom plan?{" "}
          <a href="#" className="font-medium text-emerald-600 hover:underline">
            Contact us
          </a>{" "}
          for a tailored solution.
        </p>
      </div>
    </div>
  )
}
