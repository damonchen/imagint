import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckIcon } from 'lucide-react';

const PricingPage = () => {
    const pricingPlans = [
        {
            title: 'Free',
            price: '$0',
            period: '/month',
            features: [
                'Basic features',
                'Limited usage',
                'Community support'
            ],
            buttonText: 'Get Started',
            plan: 'free'
        },
        {
            title: 'Pro',
            price: '$9.99',
            period: '/month',
            features: [
                'All Free features',
                'Advanced features',
                'Priority support',
                'API access'
            ],
            buttonText: 'Subscribe Now',
            plan: 'pro'
        },
        {
            title: 'Ultra',
            price: '$29.99',
            period: '/month',
            features: [
                'All Pro features',
                'Unlimited usage',
                'Dedicated support',
                'Custom integrations',
                'Advanced analytics'
            ],
            buttonText: 'Subscribe Now',
            plan: 'ultra'
        }
    ];

    const handleSubscribe = async (plan: string) => {
        try {
            const response = await fetch('/api/subscription/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ plan })
            });

            const data = await response.json();
            if (data.status === 'success' && data.checkoutUrl) {
                window.location.href = data.checkoutUrl;
            }
        } catch (error) {
            console.error('Subscription error:', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-12 bg-background">
            <div className="mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center">
                    <h2 className="text-3xl font-bold tracking-tight text-primary">
                        Choose Your Plan
                    </h2>
                    <p className="mt-4 text-lg text-muted-foreground">
                        Select the perfect plan for your needs
                    </p>
                </div>

                <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-6 lg:max-w-4xl lg:mx-auto xl:max-w-none xl:grid-cols-3">
                    {pricingPlans.map((plan) => (
                        <Card key={plan.title} className="flex flex-col h-full">
                            <CardHeader>
                                <CardTitle className="text-2xl font-semibold leading-6 text-primary">
                                    {plan.title}
                                </CardTitle>
                                <CardDescription className="mt-4">
                                    <span className="text-4xl font-extrabold text-primary">
                                        {plan.price}
                                    </span>
                                    <span className="text-base font-medium text-muted-foreground">
                                        {plan.period}
                                    </span>
                                </CardDescription>
                            </CardHeader>

                            <CardContent className="flex-1">
                                <ul className="space-y-4">
                                    {plan.features.map((feature) => (
                                        <li key={feature} className="flex">
                                            <CheckIcon className="flex-shrink-0 w-5 h-5 text-green-500" />
                                            <span className="ml-3 text-muted-foreground">
                                                {feature}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>

                            <CardFooter className="pt-0">
                                <Button
                                    className="w-full"
                                    onClick={() => handleSubscribe(plan.plan)}
                                >
                                    {plan.buttonText}
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default PricingPage;
