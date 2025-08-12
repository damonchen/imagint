import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import Sidebar from './sidebar'
import useIsCollapsed from '@/hooks/use-is-collapsed'
import SelfUserProvider, { useSelf } from '@/provider/self-user-provider'
import { useAuth } from '@/provider/auth-provider'
import { useEffect, useState } from 'react'

function MainContent({ isCollapsed }: { isCollapsed: boolean }) {
  const { user } = useSelf();
  const location = useLocation();

  const navigate = useNavigate();

  return <main
    id='content'
    className={`overflow-x-hidden pt-16 transition-[margin] md:overflow-y-hidden md:pt-0 ${isCollapsed ? 'md:ml-14' : 'md:ml-64'} h-full`}
  >
    <Outlet />
  </main>
}

export default function AppShell() {
  const [isCollapsed, setIsCollapsed] = useIsCollapsed()
  const { token } = useAuth();
  const isDebug = process.env.NODE_ENV === 'development';

  return (
    token || isDebug ? <div>
      <div className='relative h-full overflow-hidden bg-background'>
        <Sidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />
        <MainContent isCollapsed={isCollapsed} />
      </div>
    </div > : <>xxxxxxxxxxxx</>
  )
}
