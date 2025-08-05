import {
  Card,
  CardContent,
  // CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { useRegisterContext } from "./register-context"
import { Description, DescriptionHead, DescriptionBody, DescriptionItem, DescriptionLabel, DescriptionText, DescriptionTitle } from "@/components/custom/description";



export function StepperCompleteInfo() {
  const { invitedCode } = useRegisterContext()
  return (
    <div>
      <div className="py-2">
        <h1 className="font-semibold">Registration Complete</h1>
      </div>
      <div className={cn('grid grid-cols-1 gap-x-2 gap-y-2')}>
        <Card>
          <CardHeader>
            <CardTitle>Invitation Code</CardTitle>
          </CardHeader>
          <CardContent>
            <Description>
              <DescriptionBody className='grid-cols-1'>
                <DescriptionItem className='text-sm'>
                  <DescriptionLabel>Code:</DescriptionLabel>
                  <DescriptionText>{invitedCode}</DescriptionText>
                </DescriptionItem>
              </DescriptionBody>
            </Description>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}