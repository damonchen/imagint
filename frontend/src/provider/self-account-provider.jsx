import { useEffect, useMemo, createContext, useContext } from 'react'
import { useQueryClient, useQuery } from '@tanstack/react-query'
import { getSelf } from '@/api/account'
import { useState } from 'react'

const SelfAccountContext = createContext({})

const SelfAccountProvider = ({ children }) => {
  const queryClient = useQueryClient()
  const [refresh, setRefresh] = useState(false)
  const { data } = useQuery({
    queryKey: ['selfAccount'],
    queryFn: getSelf,
    refetchOnWindowFocus: false,
  })

  // useEffect(() => {
  //   console.log('refresh self account', refresh)
  //   queryClient.invalidateQueries({ queryKey: ['selfAccount'] })
  // }, [refresh, queryClient])

  const value = useMemo(() => {
    return {
      account: data ?? {},
      forceRefresh: () => {
        if (data) {
          setRefresh((prev) => !prev)
        }
      },
    }
  }, [data])
  return (
    <SelfAccountContext.Provider value={value}>
      {children}
    </SelfAccountContext.Provider>
  )
}
export const useSelf = () => {
  return useContext(SelfAccountContext)
}

export default SelfAccountProvider
