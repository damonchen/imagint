import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { Button } from '@/components/custom/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Case } from '@/components/case'
import Error from '@/components/error'
import { PasswordInput } from '@/components/custom/password-input'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { cn } from '@/lib/utils'
import { signIn } from '@/api/auth'
import { useAuth } from '@/provider/auth-provider'

const defaultValues = {
  email: '',
  password: '',
}

const formSchema = z.object({
  email: z
    .string()
    .min(1, { message: 'Please enter your email' })
    .email({ message: 'Invalid email address' }),
  password: z
    .string()
    .min(1, {
      message: 'Please enter your password',
    })
    .min(7, {
      message: 'Password must be at least 7 characters long',
    }),
})

export default function SignInForm({ className, ...props }) {
  const [isLoading, setIsLoading] = useState(false)
  const [hasError, setHasError] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const { setToken } = useAuth()
  const navigate = useNavigate()

  const queryClient = useQueryClient()

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues,
  })

  const mutation = useMutation({
    mutationFn: signIn,
    onSuccess: (resp) => {
      // set the token and go the next page
      console.log('mutation success', resp)
      const { access_token } = resp
      setToken(access_token)

      // 跳转到首页
      setTimeout(() => {
        // 延迟可保证access_token数据能够写入到local storage后再处理
        navigate('/');
      }, 400)
    },
    onError: (error, variables, context) => {
      console.log('resp', error, variables, context)
      setHasError(true);
      setErrorMessage('Invalid email or password')
    },
    onSettled: () => {
      setIsLoading(false)
    },
  })

  function onSubmit(data) {
    setIsLoading(true)
    mutation.mutate(data)
  }

  return (
    <div className={cn('grid gap-6', className)} {...props}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-8'>
          <div className='grid gap-2'>
            <FormField
              control={form.control}
              name='email'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder='name@expanse.com' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='password'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <div className={cn('flex items-center justify-between')}>
                    <FormLabel>Password</FormLabel>
                    <div className='text-sm text-muted-foreground'>
                      <Link
                        to='/auth/forgot-password'
                        className='ml-auto inline-block text-sm underline'
                      >
                        Forgot your password?
                      </Link>
                    </div>
                  </div>

                  <FormControl>
                    <PasswordInput placeholder='********' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <div className=''>
            <Case
              if={hasError}
              true={<Error>{errorMessage}</Error>}
              false={<></>}
            />
          </div>
          <Button type='submit' className='w-full' loading={isLoading}>
            Sign in
          </Button>
        </form>
      </Form>
    </div>
  )
}
