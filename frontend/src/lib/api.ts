import axios from 'axios'
import { ApiResponse, ApiResponseWrapper, responseInterceptor } from './api-response'

// 创建axios实例
const api = axios.create({
    baseURL: import.meta.env.VITE_PUBLIC_API_URL || '/api/v1',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器 - 统一处理响应格式
api.interceptors.response.use(
    (response) => {
        // 处理成功响应
        return responseInterceptor.onSuccess(response.data)
    },
    (error) => {
        // 处理错误响应
        const apiError = responseInterceptor.onError(error)
        return Promise.reject(apiError)
    }
)

// 封装API方法，统一返回类型
export const apiClient = {
    // GET请求
    get: async <T>(url: string, config?: any): Promise<ApiResponse<T>> => {
        try {
            const response = await api.get(url, config)
            return response
        } catch (error) {
            throw error
        }
    },

    // POST请求
    post: async <T>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
        try {
            const response = await api.post(url, data, config)
            return response
        } catch (error) {
            throw error
        }
    },

    // PUT请求
    put: async <T>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
        try {
            const response = await api.put(url, data, config)
            return response
        } catch (error) {
            throw error
        }
    },

    // DELETE请求
    delete: async <T>(url: string, config?: any): Promise<ApiResponse<T>> => {
        try {
            const response = await api.delete(url, config)
            return response
        } catch (error) {
            throw error
        }
    },

    // PATCH请求
    patch: async <T>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
        try {
            const response = await api.patch(url, data, config)
            return response
        } catch (error) {
            throw error
        }
    },
}

// 导出原始axios实例（如果需要）
export { api }

// 导出类型和工具
export type { ApiResponse }
export { ApiResponseWrapper }
