import * as React from 'react'
import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'
import { useTheme } from '../theme-provider'

const descriptionVariants = cva(
    '',
    {
        variants: {
            size: {
                default: 'h-9 px-4 py-2',
                sm: 'h-8 rounded-md px-3 text-sm',
                lg: 'h-10 rounded-md px-8',
                icon: 'h-9 w-9',
            }
        },
        defaultVariants: {
            size: 'default',
        }
    }
)

type DescriptionSize = 'default' | 'middle' | 'small'


type DescriptionLayout = 'horizontal' | 'vertical'


const DescriptionTitle = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn("font-semibold leading-none tracking-tight", className)}
        {...props}
    />
))
DescriptionTitle.displayName = 'DescriptionTitle'


const DescriptionBody = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn("grid grid-cols-3 gap-2", className)}
        {...props}
    />
))
DescriptionBody.displayName = 'DescriptionBody'


interface InternalDescriptionProps {
    size: DescriptionSize;
    bordered: boolean;
    layout: DescriptionLayout;
}

interface DescriptionProps extends Omit<
    React.ComponentPropsWithoutRef<'div'>,
    keyof InternalDescriptionProps
>, VariantProps<typeof descriptionVariants> { }

const Description = React.forwardRef<HTMLDivElement, DescriptionProps>(({ className, children, ...props }, ref) => {
    const { ...rest } =
        props as InternalDescriptionProps

    const { layout } = rest
    return (
        <div ref={ref} className={cn('flex', layout == 'horizontal' ? '' : 'flex-col', className)} >
            {children}
        </div>
    )
})

Description.displayName = 'Description'



const DescriptionHead = React.forwardRef<HTMLDivElement, DescriptionProps>(({ className, ...props }, ref) => {
    return <div
        ref={ref}
        className={cn("font-bold text-lg", className)}
        {...props}
    />
})

DescriptionHead.displayName = 'DescriptionHead'

const DescriptionLabel = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
    const {theme} = useTheme();
    return (
      <div
        ref={ref}
        className={cn(
          theme === 'light' ? 'text-gray-500' : 'text-white',
          'font-semibold',
          'mr-2',
          className
        )}
        {...props}
      />
    )
})
DescriptionLabel.displayName = 'DescriptionLabel'


const DescriptionText = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
    const { theme } = useTheme()
  return <div ref={ref} className={cn(theme === 'light' ? '' : 'text-gray-200', className)} {...props} />
})
DescriptionText.displayName = 'DescriptionText'


const DescriptionItem = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn("flex items-center text-sm py-1", className)}
        {...props}
    />
))
DescriptionItem.displayName = 'DescriptionItem'


export {
    Description,
    DescriptionHead,
    DescriptionTitle,
    DescriptionBody,
    DescriptionLabel,
    DescriptionText,
    DescriptionItem,
}