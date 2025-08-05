import * as React from 'react'
import { Button } from "@/components/custom/button"
import { Input } from '@/components/ui/input'
import { useNavigate } from "react-router-dom"
import { useRegisterContext } from "./register-context"

export function InvitedCodeForm() {
    const navigate = useNavigate();
    const { invitedCode, setInvitedCode } = useRegisterContext();
    const [isLoading, setIsLoading] = React.useState(false);

    const onInvitedCodeChange = (e) => {
        const value = e.currentTarget.value;
        if (value.length <= 6) {
            setInvitedCode(value);
        }
    }

    const onJoinClicked = () => {
        setIsLoading(true);
        // Handle join logic here
        console.log('Joining with code:', invitedCode);
    }

    return <>
        <div className="space-y-2">
            <div>Input your company invited code</div>
            <div />
            <div className='flex space-x-2'>
                <div className='w-1/3'>
                    <Input placeholder='Invited Code' value={invitedCode} onChange={onInvitedCodeChange} />
                </div>
            </div>

            <div className='flex items-center space-x-4'>
                <Button loading={isLoading} variant="default" type="submit" size='sm' onClick={onJoinClicked} disabled={invitedCode.length !== 6}>
                    Join the company
                </Button>
            </div>
        </div>
    </>
}