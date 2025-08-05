# Celery 优雅关闭解决方案

## 问题描述

在 Flask 应用中集成 Celery 后，按下 Ctrl+C 时系统无法正常关闭，这是因为：

1. **缺少信号处理器**：应用没有正确处理 SIGINT 信号（Ctrl+C）
2. **Celery 进程未优雅关闭**：Celery worker 进程仍在运行，阻止主进程退出
3. **资源未正确释放**：数据库、Redis、RabbitMQ 等连接未正确关闭

## 解决方案

### 1. 信号处理机制

在 `api_app.py` 中添加了信号处理器：

```python
def register_signal_handlers(app):
    def signal_handler(signum, frame):
        logging.info(f"收到信号 {signum}，开始关闭应用...")
        app.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill
```

### 2. 优雅关闭机制

创建了 `ApiApp` 类，包含关闭处理器注册机制：

```python
class ApiApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shutdown_handlers = []

    def register_shutdown_handler(self, handler):
        self._shutdown_handlers.append(handler)

    def shutdown(self):
        for handler in self._shutdown_handlers:
            try:
                handler()
            except Exception as e:
                logging.error(f"关闭处理器执行失败: {e}")
```

### 3. 扩展资源清理

在 `close_extensions()` 函数中处理所有扩展的关闭：

- Celery worker 关闭
- RabbitMQ 连接关闭
- Redis 连接关闭
- 数据库连接关闭

## 使用方法

### 方法 1：单独启动服务

1. **启动 Flask 应用**：

   ```bash
   python app.py
   ```

2. **启动 Celery Worker**：

   ```bash
   python celery_worker.py
   ```

3. **启动 Celery Beat**：
   ```bash
   python celery_beat.py
   ```

### 方法 2：使用服务管理器（推荐）

启动所有服务：

```bash
python start_services.py
```

这个脚本会：

- 自动启动 Flask 应用、Celery worker 和 beat
- 监控所有进程状态
- 处理 Ctrl+C 信号，优雅关闭所有服务

## 关闭应用

现在你可以通过以下方式关闭应用：

1. **Ctrl+C**：发送 SIGINT 信号，触发优雅关闭
2. **kill 命令**：发送 SIGTERM 信号

应用会：

1. 记录关闭日志
2. 关闭所有扩展连接
3. 停止 Celery worker 和 beat
4. 释放所有资源
5. 正常退出

## 日志输出

关闭时会看到类似以下的日志：

```
2024-01-01 12:00:00 - 收到信号 2，开始关闭应用...
2024-01-01 12:00:00 - 开始优雅关闭应用...
2024-01-01 12:00:00 - 关闭扩展...
2024-01-01 12:00:00 - Celery已关闭
2024-01-01 12:00:00 - RabbitMQ连接已关闭
2024-01-01 12:00:00 - Redis连接已关闭
2024-01-01 12:00:00 - 数据库连接已关闭
2024-01-01 12:00:00 - 应用关闭完成
```

## 注意事项

1. **确保环境变量正确设置**：Celery 需要正确的 broker 和 backend 配置
2. **检查依赖服务**：确保 Redis、RabbitMQ 等服务正在运行
3. **监控日志**：如果关闭时出现错误，检查日志了解具体原因
4. **进程清理**：如果仍有进程残留，可以使用 `ps aux | grep python` 查看并手动终止

## 故障排除

如果仍然无法正常关闭：

1. **检查进程**：

   ```bash
   ps aux | grep python
   ```

2. **强制终止**：

   ```bash
   kill -9 <进程ID>
   ```

3. **检查端口占用**：

   ```bash
   netstat -tulpn | grep :5080
   ```

4. **查看详细日志**：将日志级别设置为 DEBUG 以获取更多信息
