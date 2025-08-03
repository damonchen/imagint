# Pricing Features Implementation

## 功能概述

已成功实现了定价页面的交互功能，包括：

### 1. 按钮标签更新

- **Free** → **Premium**
- **Pro** → **Ultimate**
- **Enterprise** → 保持不变

### 2. 按钮点击行为

#### Premium 和 Ultimate 计划

- **未登录用户**：点击按钮会弹出登录模态框
- **已登录用户**：点击按钮会显示升级状态，然后跳转到仪表板页面

#### Enterprise 计划

- 点击按钮会打开邮件客户端，发送企业版咨询邮件

### 3. 用户体验流程

1. **未登录用户点击升级按钮**

   - 显示登录模态框
   - 用户登录成功后自动继续升级流程
   - 显示升级状态动画
   - 跳转到仪表板页面

2. **已登录用户点击升级按钮**

   - 直接显示升级状态动画
   - 2 秒后跳转到仪表板页面

3. **企业版按钮**
   - 直接打开邮件客户端
   - 预填充主题和内容

## 技术实现

### 状态管理

```typescript
const [isLoggedIn, setIsLoggedIn] = useState(false); // 用户登录状态
const [upgradingPlan, setUpgradingPlan] = useState<string | null>(null); // 升级计划状态
```

### 按钮点击处理

```typescript
const handlePricingClick = (planName: string) => {
  if (planName === t.pricing.enterprise) {
    // 企业版：发送邮件
    const subject = encodeURIComponent('Enterprise Plan Inquiry');
    const body = encodeURIComponent(
      'Hello,\n\nI am interested in your Enterprise plan...'
    );
    window.location.href = `mailto:sales@imagint.ai?subject=${subject}&body=${body}`;
  } else {
    // Premium 和 Ultimate 计划
    if (!isLoggedIn) {
      setShowSignInModal(true);
    } else {
      setUpgradingPlan(planName);
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 2000);
    }
  }
};
```

### 多语言支持

已为所有支持的语言添加了新的翻译文本：

- `upgradingToPremium`: "升级到高级版"
- `upgradingToUltimate`: "升级到终极版"
- `pleaseSignIn`: "请登录以继续"

## 文件结构

```
loading/
├── src/
│   ├── app/
│   │   ├── page.tsx              # 主页面（包含定价功能）
│   │   ├── dashboard/
│   │   │   └── page.tsx          # 仪表板页面
│   │   └── i18n/
│   │       └── translations.ts   # 翻译文件
│   └── config/
│       └── env.ts                # 环境变量配置
├── env.example                   # 环境变量示例
└── PRICING_FEATURES.md          # 本文档
```

## 测试方法

1. **启动开发服务器**

   ```bash
   npm run dev
   ```

2. **测试未登录状态**

   - 访问 http://localhost:3000
   - 滚动到定价部分
   - 点击 Premium 或 Ultimate 按钮
   - 验证登录模态框是否弹出

3. **测试登录后状态**

   - 在登录模态框中输入任意邮箱和密码
   - 点击登录按钮
   - 验证是否显示升级状态动画
   - 验证是否跳转到仪表板页面

4. **测试企业版功能**
   - 点击 Enterprise 按钮
   - 验证是否打开邮件客户端

## 环境变量配置

确保已正确配置环境变量：

```bash
# 复制环境变量示例文件
cp env.example .env.local

# 更新 .env.local 文件中的配置
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## 注意事项

1. **模拟登录状态**：当前使用 `useState` 模拟用户登录状态，实际应用中需要与后端 API 集成
2. **邮件配置**：企业版邮件地址 `sales@imagint.ai` 需要根据实际情况修改
3. **仪表板页面**：`/dashboard` 页面是简单的演示页面，实际应用中需要实现完整的用户仪表板
4. **错误处理**：已添加基本的错误处理，但可能需要根据实际 API 响应进行调整

## 后续优化建议

1. **持久化登录状态**：使用 localStorage 或 cookies 保存用户登录状态
2. **API 集成**：与真实的后端 API 集成用户认证和计划升级
3. **支付集成**：集成支付网关处理实际订阅
4. **用户仪表板**：实现完整的用户仪表板功能
5. **邮件模板**：使用更专业的邮件模板系统
