import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { authApi } from '@/lib/api'

export const AuthContext = createContext()

const AuthProvider = ({ children }) => {
  // State to hold the authentication token
  const [token, setToken_] = useState(localStorage.getItem('access_token'))

  console.log('AuthProvider token:', token)

  // Function to set the authentication token
  const setToken = (newToken) => {
    setToken_(newToken)
  }

  useEffect(() => {
    if (token) {
      // axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
      authApi.interceptors.request.use((config) => {
        config.headers.Authorization = `Bearer ${token}`
        return config
      })
      localStorage.setItem('access_token', token)
    } else {
      // delete axios.defaults.headers.common['Authorization'];
      authApi.interceptors.request.clear()
      localStorage.removeItem('access_token')
    }
  }, [token])

  // Memoized value of the authentication context
  const contextValue = useMemo(
    () => ({
      token,
      setToken,
    }),
    [token]
  )

  console.log('AuthProvider contextValue:', contextValue)

  // Provide the authentication context to the children components
  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  )
}

export const useAuth = () => {
  return useContext(AuthContext)
}

export default AuthProvider
