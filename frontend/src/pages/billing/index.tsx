import { useEffect, useState } from 'react'

import { Layout, LayoutBody, LayoutHeader } from '@/components/custom/layout'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { useQuery } from '@tanstack/react-query'

import { getSubscription } from '@/api/transaction'

// import { Search } from '@/components/search'
// import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
// import ThemeSwitch from '@/components/theme-switch'

export default function Billing() {
    // const [subscriptions, setBillings] = useState([]);

    // const { data: billingData } = useQuery({
    //     queryKey: ['subscription'],
    //     queryFn: getSubscription,
    // })

    // console.log('billing data', billingData);

    // // data billing info

    return (
        <Layout>
            <LayoutBody className='space-y-4'>
                <div>billing</div>
            </LayoutBody>
        </Layout>
    )
}

