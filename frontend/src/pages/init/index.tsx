// import { useState } from 'react'
// import ThemeSwitch from '@/components/theme-switch'
// import { UserNav } from '@/components/user-nav'
// import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
// import { Layout, LayoutBody, LayoutHeader } from '@/components/custom/layout'
// import RegisterStepper from './components/register-stepper'
// import { InvitedCodeForm } from './components/invited-code-form'
// import { RegisterProvider } from "./components/register-context"

// export default function InitPage() {
//     const [initForm, setInitForm] = useState('invitedCode')

//     const onValueChanged = (value: string) => {
//         setInitForm(value);
//     }

//     return (
//         <Layout>
//             {/* ===== Top Heading ===== */}
//             <LayoutHeader>
//                 {/* <TopNav links={topNav} /> */}
//                 <div className='ml-auto flex items-center space-x-4'>
//                     {/* <Search /> */}
//                     <ThemeSwitch />
//                     <UserNav />
//                 </div>
//             </LayoutHeader>

//             <LayoutBody className='space-y-4'>
//                 <RegisterProvider>
//                     <h1 className="flex items-center justify-center text-2xl font-bold">Welcome to use ImagInt</h1>
//                     <RadioGroup onValueChange={onValueChanged} value={initForm}>
//                         <div className="items-top flex space-x-2">
//                             <RadioGroupItem id="invitedCode" value='invitedCode' />
//                             <div className="grid gap-1.5 leading-none">
//                                 <label
//                                     htmlFor="invitedCode"
//                                     className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
//                                 >
//                                     I have an inivited code
//                                 </label>
//                             </div>
//                         </div>
//                     </RadioGroup>

//                 </RegisterProvider>
//             </LayoutBody>
//         </Layout>
//     )
// }