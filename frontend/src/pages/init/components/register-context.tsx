import * as React from 'react';
import { createContext, useContext, useMemo, useState } from "react";

type StateType = 'error' | 'loading'

type RegisterContextType = {
    invitedCode: string;
    setInvitedCode: React.Dispatch<React.SetStateAction<string>>;
    commit: () => void;
    state: StateType;
    setState: React.Dispatch<React.SetStateAction<StateType | undefined>>;
}

export const RegisterContext = createContext<RegisterContextType>({} as RegisterContextType)


export const RegisterProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [state, setState] = useState<StateType | undefined>(undefined);
    const [invitedCode, setInvitedCode] = useState('');

    const value = useMemo(() => {
        return {
            invitedCode,
            setInvitedCode,
            state,
            setState,
        }

    }, [invitedCode, state]);

    return <RegisterContext.Provider value={value} >
        {children}
    </RegisterContext.Provider >
}

export const useRegisterContext = () => {
    return useContext(RegisterContext)
}