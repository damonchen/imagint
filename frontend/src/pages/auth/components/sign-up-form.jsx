import { HTMLAttributes, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
// import { zodResolver } from '@hookform/resolvers/zod'
import { IconBrandFacebook, IconBrandGithub } from '@tabler/icons-react'
// import { z } from 'zod'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/custom/button'
import { PasswordInput } from '@/components/custom/password-input'
import { cn } from '@/lib/utils'
import { signUp } from '@/api/auth'
import { useAuth } from '@/provider/auth-provider'
import { useEffect } from 'react'


// const formSchema = z
//   .object({
//     email: z
//       .string()
//       .min(1, { message: 'Please enter your email' })
//       .email({ message: 'Invalid email address' }),
//     password: z
//       .string()
//       .min(1, {
//         message: 'Please enter your password',
//       })
//       .min(7, {
//         message: 'Password must be at least 7 characters long',
//       }),
//     confirmPassword: z.string(),
//   })
//   .refine((data) => data.password === data.confirmPassword, {
//     message: "Passwords don't match.",
//     path: ['confirmPassword'],
//   })

export function SignUpForm({ className, ...props }) {
  const [isLoading, setIsLoading] = useState(false)
  const { setToken } = useAuth()
  const navigate = useNavigate()

  const signUpMutation = useMutation({
    mutationFn: signUp,
    mutationKey: ['signUp'],
    onSuccess: (data, variables, context) => {
      // set the token and go the next page
      console.log('mutation success', data)
      const { accessToken } = data
      setToken(accessToken)

      // 跳转到首页
      setTimeout(() => {
        // 延迟可保证access_token数据能够写入到local storage后再处理
        navigate('/');
      }, 400)
    },
    onError: (error, variables, context) => {
      console.log('respone', error, variables, context)
    },
    onSettled: () => {
      setIsLoading(false);
    }
  })
 
  const form = useForm({
    defaultValues: {
      email: '',
      invitedCode: '',
      password: '',
      confirmPassword: '',
    },
  })


  function onSubmit(data) {
    setIsLoading(true)

    signUpMutation.mutate(data)
    console.log(data)

    // setTimeout(() => {
    //   setIsLoading(false)
    // }, 3000)
  }

  return (
    <div className={cn('grid gap-6', className)} {...props}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <div className='grid gap-2'>
            <FormField
              control={form.control}
              name='email'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder='name@expanse.com' {...field} {...form.register("email", {required: true})}/>
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
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <PasswordInput placeholder='********' {...field}  {...form.register("password", {required: true})}/>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='confirmPassword'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <PasswordInput placeholder='********' {...field} {...form.register("confirmPassword",  {required: true})}/>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='invitedCode'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Invited Code</FormLabel>
                  <FormControl>
                    <Input placeholder='Enter invited code if exists' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button className='mt-2' loading={isLoading}>
              Create Account
            </Button>

            <div className='relative my-2'>
              <div className='absolute inset-0 flex items-center'>
                <span className='w-full border-t' />
              </div>
              <div className='relative flex justify-center text-xs uppercase'>
                <span className='bg-background px-2 text-muted-foreground'>
                  Or continue with
                </span>
              </div>
            </div>

            <div className='flex items-center gap-2'>
              <Button
                variant='outline'
                className='w-full'
                type='button'
                loading={isLoading}
                leftSection={<IconBrandGithub className='h-4 w-4' />}
              >
                GitHub
              </Button>
              <Button
                variant='outline'
                className='w-full'
                type='button'
                loading={isLoading}
                leftSection={<IconBrandFacebook className='h-4 w-4' />}
              >
                Facebook
              </Button>
            </div>
          </div>
        </form>
      </Form>
    </div>
  )
}
