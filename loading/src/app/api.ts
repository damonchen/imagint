// pages/api/proxy/[...path].ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    // 1. 获取目标API地址 (从环境变量读取)
    const API_BASE = process.env.BACKEND_API_URL || 'https://imagint.ai/api';

    // 2. 动态构造请求路径
    const path = Array.isArray(req.query.path)
        ? req.query.path.join('/')
        : req.query.path || '';

    // 3. 拼接完整URL
    const targetUrl = `${API_BASE}/${path}?${new URLSearchParams(req.query as Record<string, string>).toString()}`;

    try {
        // 4. 转发请求到后端API
        const backendRes = await fetch(targetUrl, {
            method: req.method,
            headers: {
                ...(req.headers as Record<string, string>),
                'Content-Type': 'application/json',
                // 可添加认证头等
                Authorization: `Bearer ${process.env.API_TOKEN}`
            },
            body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined
        });

        // 5. 获取原始响应数据
        let data = await backendRes.json();

        // 6. Next.js 数据处理层 (按需修改)
        data = transformData(data); // 你的自定义处理函数

        // 7. 返回处理后的数据给前端
        res.status(backendRes.status).json(data);

    } catch (error) {
        // 8. 错误处理
        console.error('Proxy error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}

// 数据处理示例函数
function transformData(originalData: any) {
    return {
        ...originalData,
        processedAt: new Date().toISOString(),  // 添加处理时间戳
        // 其他转换逻辑...
    };
}