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

import { getBilling } from '@/api/transaction'

// import { Search } from '@/components/search'
// import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
// import ThemeSwitch from '@/components/theme-switch'

export default function Billing() {
    const [billings, setBillings] = useState([]);

    const { data: billingData } = useQuery({
        queryKey: ['billing'],
        queryFn: getBilling,
    })

    console.log('billing data', billingData);

    // data billing info

    return (
        <Layout>
            <LayoutBody className='space-y-4'>
                {
                    billings.map((billing) => {
                        return <div key={billing.id}>
                            aaaaaaaaaaa
                        </div>
                    })
                }
            </LayoutBody>
        </Layout>
    )
}

