import { useEffect, useMemo, createContext, useContext } from 'react'
import { useQueryClient, useQuery } from '@tanstack/react-query'
import { getSelf } from '@/api/user'
import { useState } from 'react'

const SelfUserContext = createContext({})

const SelfUserProvider = ({ children }) => {
  const queryClient = useQueryClient()
  const { data } = useQuery({
    queryKey: ['selfUser'],
    queryFn: getSelf,
    refetchOnWindowFocus: false,
  })

  useEffect(() => {
    queryClient.invalidateQueries({ queryKey: ['selfUser'] })
  }, [queryClient])

  const value = useMemo(() => {
    return {
      user: data?.data ?? {},
      refresh: () => {
        queryClient.invalidateQueries({ queryKey: ['selfUser'] })
      },
    }
  }, [data, queryClient])

  return (
    <SelfUserContext.Provider value={value}>
      {children}
    </SelfUserContext.Provider>
  )
}
export const useSelf = () => {
  return useContext(SelfUserContext)
}

export default SelfUserProvider
