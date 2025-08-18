import React, { useState, useCallback, createContext, useContext } from 'react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

// Context for providing the alert dialog
const AlertDialogContext = createContext(null)

// Provider component that should wrap your app or page
export function AlertDialogProvider({ children }) {
  const [dialogConfig, setDialogConfig] = useState(null)
  const [isOpen, setIsOpen] = useState(false)

  const showDialog = useCallback((config) => {
    setDialogConfig(config)
    setIsOpen(true)
  }, [])

  const hideDialog = useCallback(() => {
    setIsOpen(false)
    setDialogConfig(null)
  }, [])

  const handleConfirm = useCallback(() => {
    dialogConfig?.onConfirm?.()
    hideDialog()
  }, [dialogConfig, hideDialog])

  const handleCancel = useCallback(() => {
    dialogConfig?.onCancel?.()
    hideDialog()
  }, [dialogConfig, hideDialog])

  return (
    <AlertDialogContext.Provider value={{ showDialog, hideDialog }}>
      {children}
      <AlertDialog open={isOpen} onOpenChange={setIsOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{dialogConfig?.title}</AlertDialogTitle>
            <AlertDialogDescription>
              {dialogConfig?.description}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={handleCancel}>
              {dialogConfig?.cancelText || 'Cancel'}
            </AlertDialogCancel>
            <AlertDialogAction onClick={handleConfirm}>
              {dialogConfig?.confirmText || 'Confirm'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </AlertDialogContext.Provider>
  )
}

// The reusable hook
export function useAlertDialog(config) {
  const context = useContext(AlertDialogContext)

  if (!context) {
    throw new Error('useAlertDialog must be used within an AlertDialogProvider')
  }

  const { showDialog } = context

  const setOpen = useCallback(
    (open) => {
      if (open) {
        showDialog(config)
      }
    },
    [showDialog, config]
  )

  return { setOpen }
}
