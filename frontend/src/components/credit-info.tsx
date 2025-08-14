import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CreditCard, Image, AlertCircle } from 'lucide-react'

interface CreditInfoProps {
    balance: number
    imagesRemaining: number
    canGenerate: boolean
    onUpgrade?: () => void
}

export function CreditInfo({ balance, imagesRemaining, canGenerate, onUpgrade }: CreditInfoProps) {
    return (
        <Card className="w-full max-w-sm">
            <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-lg">
                    <CreditCard className="h-5 w-5" />
                    Credit Balance
                </CardTitle>
                <CardDescription>
                    Manage your image generation credits
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Available Credits:</span>
                    <Badge variant="secondary" className="text-lg font-bold">
                        {balance}
                    </Badge>
                </div>

                <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Images Remaining:</span>
                    <Badge variant="outline" className="flex items-center gap-1">
                        <Image className="h-3 w-3" />
                        {imagesRemaining}
                    </Badge>
                </div>

                <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status:</span>
                    {canGenerate ? (
                        <Badge variant="success" className="bg-green-100 text-green-800">
                            Ready to Generate
                        </Badge>
                    ) : (
                        <Badge variant="destructive" className="flex items-center gap-1">
                            <AlertCircle className="h-3 w-3" />
                            Insufficient Credits
                        </Badge>
                    )}
                </div>

                {!canGenerate && onUpgrade && (
                    <Button
                        onClick={onUpgrade}
                        className="w-full"
                        variant="default"
                    >
                        Upgrade Plan
                    </Button>
                )}

                <div className="text-xs text-gray-500 text-center">
                    Each image costs 4 credits
                </div>
            </CardContent>
        </Card>
    )
}
