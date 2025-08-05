import axios from 'axios'

export const controller = new AbortController()

export const appApi = axios.create({
  baseURL: import.meta.env.VITE_PUBLIC_API_URL,
  signal: controller.signal,
})

appApi.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger

    const { data, status } = response
    console.log('response data status', data, status)

    return data
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger

    console.log('reject error', error)
    // const { response } = error
    // const { status } = response
    // if (status === 401) {
    //   window.location.href = '/sign-in'
    // }

    return Promise.reject(error)
  }
)

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_PUBLIC_API_URL,
  signal: controller.signal,
  maxRate: [
    1000 * 1024, // 1000KB/s upload limit,
    1000 * 1024, // 1000KB/s download limit
  ],
})

authApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    } else {
      window.location.href = '/auth/sign-in'
    }

    config.headers['Content-Type'] = 'application/json'

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

authApi.interceptors.response.use(
  (response) => {
    const { data, status } = response
    return data
  },
  (error) => {
    console.log('reject error', error)
    const { response } = error
    const { status } = response
    if (status === 401) {
      window.location.href = '/auth/sign-in'
    }

    return Promise.reject(error)
  }
)
