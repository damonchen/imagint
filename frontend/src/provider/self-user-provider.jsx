import { useEffect, useMemo, createContext, useContext } from 'react'
import { useQueryClient, useQuery } from '@tanstack/react-query'
import { getSelf } from '@/api/user'
import { useState } from 'react'

const SelfUserContext = createContext({})

const SelfUserProvider = ({ children }) => {
  const queryClient = useQueryClient()
  const [refresh, setRefresh] = useState(false)
  const { data } = useQuery({
    queryKey: ['selfUser'],
    queryFn: getSelf,
    refetchOnWindowFocus: false,
  })

  // useEffect(() => {
  //   console.log('refresh self user', refresh)
  //   queryClient.invalidateQueries({ queryKey: ['selfUser'] })
  // }, [refresh, queryClient])

  const value = useMemo(() => {
    return {
      user: data ?? {},
      forceRefresh: () => {
        if (data) {
          setRefresh((prev) => !prev)
        }
      },
    }
  }, [data])
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
