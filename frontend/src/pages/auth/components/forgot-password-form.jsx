import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
// import { toast } from '@/components/ui/toast'
import useToast from '@/hooks/use-toast'
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
import { use } from 'react'

const defaultValues = {
  email: '',
}

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState('')

  const toast = useToast()

  const form = useForm({
    defaultValues,
  })

  function onSubmit(data) {
    toast({
      title: 'You submitted the following values:',
      description: (
        <pre className='mt-2 w-[340px] rounded-md bg-slate-950 p-4'>
          <code className='text-white'>{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-8'>
        <FormField
          control={form.control}
          name='email'
          render={({ field }) => (
            <FormItem>
              <div className={cn('flex items-center')}>
                <FormLabel>Email</FormLabel>
                <Link
                  to='/#/auth/sign-in'
                  className='ml-auto inline-block text-sm underline'
                >
                  Back to sign in
                </Link>
              </div>
              <FormControl>
                <Input
                  placeholder='me@expanse.com'
                  {...field}
                  required
                  value={email}
                />
              </FormControl>
              <FormDescription>
                You will receive a captcha code to reset the password. Please
                check your mail box.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type='button' className='w-full'>
          Send
        </Button>
      </form>
    </Form>
  )
}
