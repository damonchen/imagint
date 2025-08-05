

export default function Error({children}: {children:React.ReactNode}) {
  return <div className='flex items-center text-red-500'>{children}</div>
}