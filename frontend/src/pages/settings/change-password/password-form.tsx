import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/custom/button"
import { changePassword } from "@/api/user"
import { useMutation } from "@tanstack/react-query"
import { useState } from "react"
import { useToast } from '@/hooks/use-toast'

const passwordFormSchema = z.object({
    oldPassword: z.string().min(6, {
        message: "Password must be at least 6 characters",
    }),
    newPassword: z.string().min(6, {
        message: "Password must be at least 6 characters",
    }),
    confirmedNewPassword: z.string().min(6, {
        message: "Password must be at least 6 characters",
    }),
})

type PasswordFormValues = z.infer<typeof passwordFormSchema>

const defaultValues: Partial<PasswordFormValues> = {
    oldPassword: '',
    newPassword: '',
    confirmedNewPassword: '',
}

export function PasswordForm() {
    const [isLoading, setIsLoading] = useState(false)
    const { toast } = useToast()

    const form = useForm<PasswordFormValues>({
        resolver: zodResolver(passwordFormSchema),
        defaultValues,
    })

    const passwordMutation = useMutation({
        mutationFn: changePassword,
        mutationKey: ['signUp'],
        onSettled: () => {
            setIsLoading(false)
        },

    })

    function onSubmit(data: PasswordFormValues) {
        setIsLoading(true);
        passwordMutation.mutate(data, {
            onSuccess: (resp) => {
                console.log('resp', resp);

                if (resp.status === 'ok') {
                    toast({
                        title: 'Password changed successfully',
                    })
                } else {
                    toast({
                        title: 'Password change failed',
                        description: resp.message,
                    })
                }
            }
        });

        // toast({
        //     title: 'You submitted the following values:',
        //     description: (
        //         <pre className='mt-2 w-[340px] rounded-md bg-slate-950 p-4'>
        //             <code className='text-white'>{JSON.stringify(data, null, 2)}</code>
        //         </pre>
        //     ),
        // })
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-8'>
                <FormField
                    control={form.control}
                    name='oldPassword'
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>OldPassword</FormLabel>
                            <FormControl>
                                <Input placeholder='********' {...field} type="password" />
                            </FormControl>
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name='newPassword'
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>New Password</FormLabel>
                            <FormControl>
                                <Input placeholder='********' {...field} type="password" />
                            </FormControl>
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name='confirmedNewPassword'
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Confirmed New Password</FormLabel>
                            <FormControl>
                                <Input placeholder='********' {...field} type="password" />
                            </FormControl>
                        </FormItem>
                    )}
                />

                <Button type='submit' loading={isLoading}>Change Password</Button>
            </form>
        </Form>
    )
}