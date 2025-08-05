import { createHashRouter } from 'react-router-dom'
import GeneralError from './pages/errors/general-error'
import NotFoundError from './pages/errors/not-found-error'
import MaintenanceError from './pages/errors/maintenance-error'

const router = createHashRouter([
  // Auth routes
  {
    path: '/auth/sign-in',
    lazy: async () => ({
      Component: (await import('./pages/auth/sign-in')).default,
    }),
  },
  // {
  //   path: '/sign-in-2',
  //   lazy: async () => ({
  //     Component: (await import('./pages/auth/sign-in-2')).default,
  //   }),
  // },
  {
    path: '/auth/sign-up',
    lazy: async () => ({
      Component: (await import('./pages/auth/sign-up')).default,
    }),
  },
  {
    path: '/auth/forgot-password',
    lazy: async () => ({
      Component: (await import('./pages/auth/forgot-password')).default,
    }),
  },
  // {
  //   path: '/otp',
  //   lazy: async () => ({
  //     Component: (await import('./pages/auth/otp')).default,
  //   }),
  // },

  // Main routes
  {
    path: '/',
    lazy: async () => {
      const AppShell = await import('./components/app-shell')
      return { Component: AppShell.default }
    },
    // errorElement: <GeneralError />,
    children: [
      {
        index: true,
        lazy: async () => ({
          Component: (await import('./pages/dashboard')).default,
        }),
      },
      // {
      //   path: 'init',
      //   lazy: async () => ({
      //     Component: (await import('./pages/init')).default,
      //   }),
      // },
      // {
      //   path: 'invite',
      //   lazy: async () => ({
      //     Component: (await import('./pages/init/invite')).default,
      //   }),
      // },
      // {
      //   path: 'company/new',
      //   lazy: async () => ({
      //     Component: (await import('./pages/init/new-company')).default,
      //   }),
      // },
      // {
      //   path: 'ticket',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/tickets')).default,
      //   }),
      // },
      // {
      //   path: 'company',
      //   lazy: async () => ({
      //     // Component: (await import('@/components/coming-soon')).default,
      //     Component: (await import('@/pages/company')).default,
      //   }),
      //   errorElement: <GeneralError />,
      //   children: [
      //     {
      //       index: true,
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/profile')).default,
      //       }),
      //     },
      //     {
      //       path: 'account',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/account')).default,
      //       }),
      //     },
      //     {
      //       path: 'role',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/role')).default,
      //       }),
      //     },
      //     {
      //       path: 'position',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/position')).default,
      //       }),
      //     },
      //     {
      //       path: 'project',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/project')).default,
      //       }),
      //     },
      //     {
      //       path: 'appearance',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/appearance')).default,
      //       }),
      //     },
      //     {
      //       path: 'notifications',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/notifications'))
      //           .default,
      //       }),
      //     },
      //     {
      //       path: 'display',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/display')).default,
      //       }),
      //     },
      //     {
      //       path: 'error-example',
      //       lazy: async () => ({
      //         Component: (await import('./pages/company/error-example'))
      //           .default,
      //       }),
      //       errorElement: <GeneralError className='h-[50svh]' minimal />,
      //     },
      //   ],
      // },
      // {
      //   path: 'company/new',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/company/new')).default,
      //   }),
      // },
      // {
      //   path: 'workflows',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/workflows')).default,
      //   }),
      // },
      // {
      //   path: 'workflows/new',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/workflows/new')).default,
      //   }),
      // },
      // {
      //   path: 'workflows/:workflowId',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/workflows/views')).default,
      //   }),
      // },
      // {
      //   path: 'users',
      //   lazy: async () => ({
      //     Component: (await import('@/components/coming-soon')).default,
      //   }),
      // },
      // {
      //   path: 'analysis',
      //   lazy: async () => ({
      //     Component: (await import('@/components/coming-soon')).default,
      //   }),
      // },
      // {
      //   path: 'extra-components',
      //   lazy: async () => ({
      //     Component: (await import('@/pages/extra-components')).default,
      //   }),
      // },
      {
        path: 'settings',
        lazy: async () => ({
          Component: (await import('./pages/settings')).default,
        }),
        errorElement: <GeneralError />,
        children: [
          {
            index: true,
            lazy: async () => ({
              Component: (await import('./pages/settings/profile')).default,
            }),
          },
          {
            path: 'account',
            lazy: async () => ({
              Component: (await import('./pages/settings/account')).default,
            }),
          },
          {
            path: 'appearance',
            lazy: async () => ({
              Component: (await import('./pages/settings/appearance')).default,
            }),
          },
          {
            path: 'notifications',
            lazy: async () => ({
              Component: (await import('./pages/settings/notifications'))
                .default,
            }),
          },
          {
            path: 'display',
            lazy: async () => ({
              Component: (await import('./pages/settings/display')).default,
            }),
          },
          {
            path: 'error-example',
            lazy: async () => ({
              Component: (await import('./pages/settings/error-example'))
                .default,
            }),
            errorElement: <GeneralError className='h-[50svh]' minimal />,
          },
        ],
      },
      {
        path: 'billing',
        lazy: async () => ({
          Component: (await import('./pages/billing')).default,
        }),
      }
    ],
  },

  // Error routes
  { path: '/500', Component: GeneralError },
  { path: '/404', Component: NotFoundError },
  { path: '/503', Component: MaintenanceError },

  // Fallback 404 route
  { path: '*', Component: NotFoundError },
])

export default router
