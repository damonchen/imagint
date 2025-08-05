import { useState } from 'react'

import { Layout, LayoutBody, LayoutHeader } from '@/components/custom/layout'
import { Search } from '@/components/search'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import ThemeSwitch from '@/components/theme-switch'
import { TopNav } from '@/components/top-nav'
import { UserNav } from '@/components/user-nav'

export default function Billing() {

    return (
        <Layout>
            {/* ===== Top Heading ===== */}
            <LayoutHeader>
                {/* <TopNav links={topNav} /> */}
                <div className='ml-auto flex items-center space-x-4'>
                    <Search />
                    <ThemeSwitch />
                    <UserNav />
                </div>
            </LayoutHeader>
            <LayoutBody className='space-y-4'>
            </LayoutBody>
        </Layout>
    )
}

