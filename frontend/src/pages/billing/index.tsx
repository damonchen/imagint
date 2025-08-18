import { useEffect, useState, useMemo, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { toast } from '@/hooks/use-toast'
import {
    CreditCard,
    Crown,
    Zap,
    X,
    ChevronLeft,
    ChevronRight,
    ChevronFirst,
    ChevronLast,
} from 'lucide-react'

import { Layout, LayoutBody } from '@/components/custom/layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'

import { getUserCredits, getSubscriptionPlans, getUserCreditTransactions } from '@/api/credit'
import { getSubscriptions, cancelSubscription, createSubscription } from '@/api/subscription'
import { useUserStore } from '@/store/user'
import { useAlertDialog } from '@/provider/alert-dialog-provider'

// 订阅计划类型
const PLAN_TYPES = {
    PRO: 'pro',
    ULTRA: 'ultra'
}

// 计划配置
const PLAN_CONFIG = {
    [PLAN_TYPES.PRO]: {
        name: 'Pro',
        price: 29,
        credits: 1000,
        icon: <Zap className="h-4 w-4" />,
        color: 'bg-blue-500'
    },
    [PLAN_TYPES.ULTRA]: {
        name: 'Ultra',
        price: 99,
        credits: 5000,
        icon: <Crown className="h-4 w-4" />,
        color: 'bg-purple-500'
    }
}

export default function Billing() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const { credit, setCredit } = useUserStore()

    // 状态管理
    const [currentPage, setCurrentPage] = useState(1)
    const [pageSize, setPageSize] = useState(10)

    const { setOpen: setAlertOpen } = useAlertDialog({
        title: "Subscription Cancel",
        description: "Are you sure you want to cancel your subscription?",
        confirmText: "Yes, cancel",
        cancelText: "No, keep it",
        onConfirm: () => {
            // console.log('yes confirm');
            cancelSubscriptionMutation.mutate(activeSubscription.id)
        }
    })

    // 获取用户credit信息
    const { data: creditInfo } = useQuery({
        queryKey: ['userCredits'],
        queryFn: getUserCredits,
        refetchOnWindowFocus: false,
    })

    // 获取订阅计划
    const { data: plansData } = useQuery({
        queryKey: ['subscriptionPlans'],
        queryFn: getSubscriptionPlans,
        refetchOnWindowFocus: false,
    })

    // 获取用户订阅信息
    const { data: subscriptionsData } = useQuery({
        queryKey: ['subscriptions'],
        queryFn: getSubscriptions,
        refetchOnWindowFocus: false,
    })

    // 获取交易记录
    const { data: transactionsData, isLoading: transactionsLoading } = useQuery({
        queryKey: ['userCreditTransactions', currentPage, pageSize],
        queryFn: () => getUserCreditTransactions(currentPage, pageSize),
        // refetchOnWindowFocus: false,
    })

    // 取消订阅mutation
    const cancelSubscriptionMutation = useMutation({
        mutationFn: cancelSubscription,
        onSuccess: () => {
            toast({
                title: "Subscription Cancelled",
                description: "Your subscription has been cancelled successfully.",
            })
            queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
        },
        onError: (error) => {
            toast({
                title: "Error",
                description: error.message || "Failed to cancel subscription.",
                variant: "destructive"
            })
        }
    })

    // 更新credit信息
    useEffect(() => {
        if (creditInfo) {
            setCredit(creditInfo.data)
        }
    }, [creditInfo, setCredit])

    const activeSubscription = useMemo(() => {
        const subscriptions = subscriptionsData?.data || [];

        if (!subscriptions || !subscriptions.length) return null

        const activeSubscription = subscriptions.find(sub => sub.status === 'active')
        return activeSubscription;
    }, [subscriptionsData])

    // 获取当前用户计划类型
    const getCurrentPlanType = useCallback(() => {
        if (!activeSubscription) return null

        console.log('activeSubscription.planId:', activeSubscription.planId)
        const plans = plansData.data.plans || [];

        console.log('plans:', plans)

        const planId = parseInt(activeSubscription.planId, 10)
        console.log('Parsed planId:', planId)

        const plan = plans.find((plan) => plan.id === planId);
        console.log('Filtered plan:', plan)
        return plan?.name || null;

    }, [plansData, activeSubscription]);

    const currentPlanType = useMemo(() => getCurrentPlanType(), [getCurrentPlanType])

    // 处理升级计划
    const handleUpgrade = async (planType: string) => {
        try {
            const response = await createSubscription(planType)
            if (response.status === "fail") {
                toast({
                    title: "Error",
                    description: response.message,
                    variant: "destructive"
                })
                return;
            }
            const session = response.data

            if (session?.checkoutUrl) {
                window.location.href = session.checkoutUrl
            } else {
                toast({
                    title: "Error",
                    description: "Failed to get checkout URL.",
                    variant: "destructive"
                })
            }
        } catch (error) {
            toast({
                title: "Error",
                description: error.message || "Failed to upgrade plan.",
                variant: "destructive"
            })
        }
    }

    // 处理取消订阅
    const handleCancelSubscription = async () => {
        if (!activeSubscription) return

        setAlertOpen(true)

        // if (confirm('Are you sure you want to cancel your subscription?')) {
        //     cancelSubscriptionMutation.mutate(activeSubscription.id)
        // }
    }

    // 渲染升级按钮
    const renderUpgradeButtons = () => {
        if (currentPlanType === PLAN_TYPES.ULTRA) {
            return null // Ultra用户不需要升级按钮
        }

        return (
            <div className="flex gap-2">
                {currentPlanType !== PLAN_TYPES.PRO && (
                    <Button
                        onClick={() => handleUpgrade(PLAN_TYPES.PRO)}
                        className="bg-blue-500 hover:bg-blue-600"
                        size="sm"
                    >
                        <Zap className="h-4 w-4 mr-2" />
                        Upgrade Pro
                    </Button>
                )}
                <Button
                    onClick={() => handleUpgrade(PLAN_TYPES.ULTRA)}
                    className="bg-purple-500 hover:bg-purple-600"
                    size="sm"
                >
                    <Crown className="h-4 w-4 mr-2" />
                    Upgrade Ultra
                </Button>
            </div>
        )
    }

    // 渲染取消订阅按钮
    const renderCancelButton = () => {
        if (!currentPlanType) return null

        return (
            <Button
                onClick={handleCancelSubscription}
                variant="outline"
                size="sm"
                disabled={cancelSubscriptionMutation.isPending}
            >
                <X className="h-4 w-4 mr-2" />
                {cancelSubscriptionMutation.isPending ? 'Cancelling...' : 'Cancel Subscription'}
            </Button>
        )
    }

    // 分页处理
    const totalPages = transactionsData?.data?.totalPages || 1
    const totalItems = transactionsData?.data?.total || 0

    const handlePageChange = (page) => {
        setCurrentPage(page)
    }

    const handlePageSizeChange = (size) => {
        setPageSize(size)
        setCurrentPage(1)
    }

    // 截断提示词
    const truncatePrompt = (prompt, maxLength = 20) => {
        if (!prompt || prompt.length <= maxLength) return prompt
        return prompt.substring(0, maxLength) + '...'
    }

    return (
        <Layout>
            <LayoutBody className='space-y-6'>
                {/* 页面标题 */}
                <div className="space-y-2">
                    <h1 className="text-3xl font-bold tracking-tight">Billing & Usage</h1>
                    <p className="text-muted-foreground">
                        Manage your subscription and view usage history
                    </p>
                </div>

                {/* 顶部Card */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2">
                                    <CreditCard className="h-5 w-5 text-primary" />
                                    <span className="text-sm font-medium text-muted-foreground">
                                        Current Plan
                                    </span>
                                    <span>
                                        {{ free: 'Free', pro: 'Pro', ultra: 'Ultra' }[currentPlanType] || 'Free'}
                                    </span>
                                </div>
                                <div className="flex items-baseline gap-2">
                                    <span className="text-3xl font-bold">
                                        {credit?.balance || 0}
                                    </span>
                                    <span className="text-sm text-muted-foreground">credits remaining</span>
                                </div>
                                {currentPlanType && (
                                    <Badge variant="secondary" className="w-fit">
                                        {PLAN_CONFIG[currentPlanType]?.icon}
                                        {PLAN_CONFIG[currentPlanType]?.name} Plan
                                    </Badge>
                                )}
                            </div>

                            <div className="flex items-center gap-3">
                                {renderUpgradeButtons()}
                                {renderCancelButton()}
                            </div>
                        </div>
                    </CardHeader>
                </Card>

                {/* 交易记录Table */}
                <Card>
                    <CardHeader>
                        <CardTitle>Usage History</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {/* 分页控制 */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <span className="text-sm text-muted-foreground">Show</span>
                                    <select
                                        value={pageSize}
                                        onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                                        className="border rounded px-2 py-1 text-sm"
                                    >
                                        <option value={10}>10</option>
                                        <option value={20}>20</option>
                                        <option value={50}>50</option>
                                    </select>
                                    <span className="text-sm text-muted-foreground">entries</span>
                                </div>

                                <div className="text-sm text-muted-foreground">
                                    Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, totalItems)} of {totalItems} entries
                                </div>
                            </div>

                            {/* Table */}
                            <div className="border rounded-lg">
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Date</TableHead>
                                            <TableHead>Prompt</TableHead>
                                            <TableHead>Images</TableHead>
                                            <TableHead>Size</TableHead>
                                            <TableHead>Credits Used</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {transactionsLoading ? (
                                            <TableRow>
                                                <TableCell colSpan={6} className="text-center py-8">
                                                    Loading...
                                                </TableCell>
                                            </TableRow>
                                        ) : transactionsData?.items?.length > 0 ? (
                                            transactionsData.items.map((transaction) => (
                                                <TableRow key={transaction.id}>
                                                    <TableCell className="font-medium">
                                                        {new Date(transaction.createdAt).toLocaleDateString()}
                                                    </TableCell>
                                                    <TableCell>
                                                        <TooltipProvider>
                                                            <Tooltip>
                                                                <TooltipTrigger asChild>
                                                                    <span className="cursor-help">
                                                                        {truncatePrompt(transaction.prompt)}
                                                                    </span>
                                                                </TooltipTrigger>
                                                                <TooltipContent>
                                                                    <p className="max-w-xs">{transaction.prompt}</p>
                                                                </TooltipContent>
                                                            </Tooltip>
                                                        </TooltipProvider>
                                                    </TableCell>
                                                    <TableCell>{transaction.imageCount || 1}</TableCell>
                                                    <TableCell>{transaction.size || '1:1'}</TableCell>
                                                    <TableCell>{transaction.creditsUsed || 4}</TableCell>
                                                </TableRow>
                                            ))
                                        ) : (
                                            <TableRow>
                                                <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                                                    No transactions found
                                                </TableCell>
                                            </TableRow>
                                        )}
                                    </TableBody>
                                </Table>
                            </div>

                            {/* 分页导航 */}
                            {totalPages > 1 && (
                                <div className="flex items-center justify-center gap-2">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handlePageChange(1)}
                                        disabled={currentPage === 1}
                                    >
                                        <ChevronFirst className="h-4 w-4" />
                                    </Button>

                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handlePageChange(currentPage - 1)}
                                        disabled={currentPage === 1}
                                    >
                                        <ChevronLeft className="h-4 w-4" />
                                    </Button>

                                    <div className="flex items-center gap-1">
                                        {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                                            let pageNum
                                            if (totalPages <= 5) {
                                                pageNum = i + 1
                                            } else if (currentPage <= 3) {
                                                pageNum = i + 1
                                            } else if (currentPage >= totalPages - 2) {
                                                pageNum = totalPages - 4 + i
                                            } else {
                                                pageNum = currentPage - 2 + i
                                            }

                                            return (
                                                <Button
                                                    key={pageNum}
                                                    variant={currentPage === pageNum ? "default" : "outline"}
                                                    size="sm"
                                                    onClick={() => handlePageChange(pageNum)}
                                                    className="w-8 h-8 p-0"
                                                >
                                                    {pageNum}
                                                </Button>
                                            )
                                        })}
                                    </div>

                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handlePageChange(currentPage + 1)}
                                        disabled={currentPage === totalPages}
                                    >
                                        <ChevronRight className="h-4 w-4" />
                                    </Button>

                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handlePageChange(totalPages)}
                                        disabled={currentPage === totalPages}
                                    >
                                        <ChevronLast className="h-4 w-4" />
                                    </Button>
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </LayoutBody>
        </Layout>
    )
}

