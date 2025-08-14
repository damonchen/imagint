// API响应类型定义
export interface ApiResponse<T = any> {
    status: 'ok' | 'error' | 'limit';
    message?: string;
    data: T;
}

// API错误类型
export interface ApiError {
    status: 'error' | 'limit';
    message: string;
    data?: any;
}

// 统一响应包装器
export class ApiResponseWrapper {
    static success<T>(data: T, message?: string): ApiResponse<T> {
        return {
            status: 'ok',
            message,
            data
        };
    }

    static error(message: string, data?: any): ApiResponse {
        return {
            status: 'error',
            message,
            data
        };
    }

    static limit(message: string, data?: any): ApiResponse {
        return {
            status: 'limit',
            message,
            data
        };
    }

    // 检查响应状态
    static isSuccess(response: ApiResponse): boolean {
        return response.status === 'ok';
    }

    static isError(response: ApiResponse): boolean {
        return response.status === 'error';
    }

    static isLimit(response: ApiResponse): boolean {
        return response.status === 'limit';
    }

    // 从响应中提取数据
    static getData<T>(response: ApiResponse<T>): T {
        return response.data;
    }

    // 从响应中提取错误信息
    static getMessage(response: ApiResponse): string {
        return response.message || 'Unknown error';
    }
}

// 响应拦截器
export const responseInterceptor = {
    // 处理成功响应
    onSuccess: <T>(response: any): ApiResponse<T> => {
        // 如果响应已经是包装过的格式，直接返回
        if (response && typeof response === 'object' && 'status' in response) {
            return response;
        }

        // 否则包装成成功响应
        return ApiResponseWrapper.success(response);
    },

    // 处理错误响应
    onError: (error: any): ApiResponse => {
        if (error.response) {
            const { status, data } = error.response;

            // 处理不同的HTTP状态码
            if (status === 429) {
                return ApiResponseWrapper.limit('Rate limit exceeded. Please try again later.');
            }

            if (status === 400) {
                return ApiResponseWrapper.error(data?.message || 'Bad request');
            }

            if (status === 401) {
                return ApiResponseWrapper.error('Unauthorized. Please login again.');
            }

            if (status === 403) {
                return ApiResponseWrapper.error('Forbidden. You do not have permission.');
            }

            if (status === 404) {
                return ApiResponseWrapper.error('Resource not found.');
            }

            if (status >= 500) {
                return ApiResponseWrapper.error('Server error. Please try again later.');
            }
        }

        // 网络错误或其他错误
        if (error.code === 'NETWORK_ERROR') {
            return ApiResponseWrapper.error('Network error. Please check your connection.');
        }

        return ApiResponseWrapper.error(error.message || 'Unknown error occurred.');
    }
};
