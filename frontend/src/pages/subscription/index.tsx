import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useMutation } from '@tanstack/react-query'
import { createSubscription, getPlan } from '@/api/subscription'
import { useToast } from '@/hooks/use-toast'
import { useSelf } from '@/provider/self-user-provider'

export default function SubscriptionPage() {
    /// 从请求中获取plan名称
    const { plan } = useParams()

    const [isLoading, setIsLoading] = useState(false)
    const { user } = useSelf()
    const navigate = useNavigate()
    const { toast } = useToast()

    // 此处有待优化，不同的订阅类型使用不同的数据类型

    const [data, setData] = useState({
        plan: 'pro',
        billing_period: 'monthly',
        price: 29.99,
        currency: 'USD',
        user_id: user?.id,
    })

    const subscriptionMutation = useMutation({
        mutationKey: ['createSubscription'],
        mutationFn: createSubscription,
        onSettled: () => {
            setIsLoading(false)
        }
    })

    useEffect(() => {
        if (plan) {
            getPlan(plan).then((resp) => {
                if (resp.status === 'ok') {
                    setData(resp.data)
                }
            })
        }
    }, [plan])

    const handleSubscribe = () => {
        setIsLoading(true)
        subscriptionMutation.mutate(data, {
            onSuccess: (resp) => {
                if (resp.status === 'ok') {
                    const data = resp.data;
                    const { checkoutUrl } = data

                    window.location.href = checkoutUrl;

                    // toast({
                    //     title: 'Subscription created successfully',
                    //     description: 'Redirecting to payment page...'
                    // })
                } else {
                    toast({
                        title: 'Failed to create subscription',
                        description: resp.message,
                        variant: 'destructive'
                    })
                }
            },
            onError: (error) => {
                toast({
                    title: 'Failed to create subscription',
                    description: error.message,
                    variant: 'destructive'
                })
            }
        })
    };

    return (
        <div className="container mx-auto py-8">
            <div className="flex gap-8">
                {/* Left section - 2/3 width */}
                <div className="w-2/3">
                    <Card>
                        <CardHeader>
                            <CardTitle>Premium Subscription</CardTitle>
                            <CardDescription>
                                Get access to all premium features and benefits
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <h3 className="text-lg font-semibold">Features included:</h3>
                                <ul className="list-disc list-inside space-y-1">
                                    <li>Unlimited access to all content</li>
                                    <li>Priority customer support</li>
                                    <li>Advanced analytics and reporting</li>
                                    <li>Custom integrations</li>
                                    <li>Team collaboration tools</li>
                                </ul>
                            </div>

                            <div className="space-y-2">
                                <h3 className="text-lg font-semibold">Additional Benefits:</h3>
                                <p className="text-muted-foreground">
                                    Subscribe now and get 30 days free trial with money-back guarantee.
                                    Cancel anytime during the trial period.
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Right section - 1/3 width */}
                <div className="w-1/3">
                    <Card>
                        <CardHeader>
                            <CardTitle>Subscription Details</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex justify-between">
                                <span>Plan</span>
                                <span className="font-semibold">Premium</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Billing Period</span>
                                <span className="font-semibold">Monthly</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Price</span>
                                <span className="font-semibold">$29.99/month</span>
                            </div>
                            <div className="border-t pt-4">
                                <div className="flex justify-between text-lg font-bold">
                                    <span>Total</span>
                                    <span>$29.99</span>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full"
                                onClick={handleSubscribe}
                                disabled={subscriptionMutation.isPending}
                            >
                                {subscriptionMutation.isPending ? 'Processing...' : 'Subscribe Now'}
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            </div>
        </div>
    )
}
