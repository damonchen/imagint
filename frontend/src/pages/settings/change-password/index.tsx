import { PasswordForm } from './password-form'
import { Separator } from '@/components/ui/separator'

export default function SettingsAppearance() {
    return (
        <div className='space-y-6'>
            <div>
                <h3 className='text-lg font-medium'>Change Password</h3>
                <p className='text-sm text-muted-foreground'>
                    Change your password. Please enter your old password and new password. Password length must be at least 8 characters.
                </p>
            </div>
            <Separator />
            <PasswordForm />
        </div>
    )
}
