// 测试API拦截器是否正确处理后端响应格式
import { appApi, authApi } from './api'

// 模拟后端响应数据
const mockBackendResponse = {
  data: {
    id: 1,
    name: 'test',
    items: [1, 2, 3],
  },
}

const mockDirectResponse = {
  id: 1,
  name: 'test',
  items: [1, 2, 3],
}

// 测试函数
export function testApiInterceptors() {
  console.log('Testing API interceptors...')

  // 模拟axios响应对象
  const mockResponse = {
    data: mockBackendResponse,
    status: 200,
  }

  // 测试appApi拦截器
  const appApiResult =
    appApi.interceptors.response.handlers[0].fulfilled(mockResponse)
  console.log('appApi result:', appApiResult)
  console.log('Expected:', mockBackendResponse.data)
  console.log('Test passed:', appApiResult === mockBackendResponse.data)

  // 测试直接返回数据的情况
  const mockDirectResponseObj = {
    data: mockDirectResponse,
    status: 200,
  }

  const appApiDirectResult = appApi.interceptors.response.handlers[0].fulfilled(
    mockDirectResponseObj
  )
  console.log('appApi direct result:', appApiDirectResult)
  console.log('Expected:', mockDirectResponse)
  console.log('Test passed:', appApiDirectResult === mockDirectResponse)

  // 测试authApi拦截器
  const authApiResult =
    authApi.interceptors.response.handlers[0].fulfilled(mockResponse)
  console.log('authApi result:', authApiResult)
  console.log('Expected:', mockBackendResponse.data)
  console.log('Test passed:', authApiResult === mockBackendResponse.data)
}

// 导出测试函数
export default testApiInterceptors
