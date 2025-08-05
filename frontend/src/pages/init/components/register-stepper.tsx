import { useState, useMemo, useEffect } from "react"
import {
    Step,
    Stepper,
    useStepper,
    type StepItem,
} from "@/components/stepper"
import { useMutation } from "@tanstack/react-query"
import { Button } from "@/components/custom/button"
import { StepperCompleteInfo } from "./stepper-complete-info"

import { useRegisterContext } from "./register-context"
import { useNavigate } from "react-router-dom"

export default function RegisterStepper() {
    const {
        state,
    } = useRegisterContext();

    const steps = useMemo(() => {
        const steps = [
            { label: "Enter Invitation Code", id: 'invite', icon: '' },
        ] satisfies StepItem[]

        return steps;
    }, [])

    return (<>
        <div className="flex w-full flex-col gap-4">

            <Stepper initialStep={0} steps={steps} state={state}>
                {steps.map(({ label, id, icon }) => {
                    return (
                        <Step key={id} label={label} icon={icon}>
                            <div className="my-4 border bg-secondary text-primary rounded-md">
                                <div className="p-4">
                                    <h2>Please enter your invitation code to continue</h2>
                                </div>
                            </div>
                        </Step>
                    )
                })}
                <Footer />
            </Stepper>

        </div>
    </>)
}

const Footer = () => {
    const {
        currentStep,
        nextStep,
        prevStep,
        // resetSteps,
        isDisabledStep,
        hasCompletedAllSteps,
        isLastStep,
        isOptionalStep,
    } = useStepper()

    const { state, setState } = useRegisterContext();
    const navigate = useNavigate();

    const loading = useMemo(() => state === 'loading', [state]);

    useEffect(() => {
    }, [])

    const onCommitClick = () => {
        // Handle commit logic here
    }

    const onNextClick = () => {
        nextStep();
    }

    return (
        <>
            {hasCompletedAllSteps && (
                <div className='bg-secondary border text-primary rounded-sm p-4'>
                    <StepperCompleteInfo />
                </div>
            )}
            <div className="w-full flex justify-end gap-2">
                {hasCompletedAllSteps ? (
                    <>
                        <Button
                            disabled={isDisabledStep}
                            onClick={prevStep}
                            size="sm"
                            variant="secondary"
                        >
                            Prev
                        </Button>
                        <Button size="sm" onClick={onCommitClick} loading={loading}>
                            Commit
                        </Button>
                    </>
                ) : (
                    <>
                        <Button
                            disabled={isDisabledStep}
                            onClick={prevStep}
                            size="sm"
                            variant="secondary"
                        >
                            Prev
                        </Button>
                        <Button size="sm" onClick={onNextClick}>
                            {isLastStep ? "Finish" : isOptionalStep ? "Skip" : "Next"}
                        </Button>
                    </>
                )}
            </div>
        </>
    )
}