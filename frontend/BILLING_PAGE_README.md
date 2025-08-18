# Billing页面功能说明

## 功能概述

Billing页面是一个完整的订阅管理和使用记录查看页面，包含以下主要功能：

### 1. 顶部Credit信息Card

#### 布局结构

- **左侧**：显示当前用户剩余的credit数量（加粗显示）
- **右侧**：根据用户当前计划显示不同的按钮

#### 按钮逻辑

- **普通用户**：显示 "Upgrade Pro" 和 "Upgrade Ultra" 按钮
- **Pro用户**：显示 "Upgrade Ultra" 按钮
- **Ultra用户**：不显示升级按钮
- **所有付费用户**：显示 "Cancel Subscription" 按钮

#### 视觉设计

- 使用Card组件包装，提供清晰的视觉层次
- Credit数量使用大字体加粗显示
- 当前计划使用Badge组件标识
- 按钮使用不同的颜色区分（Pro: 蓝色，Ultra: 紫色）

### 2. 升级功能

#### 升级流程

1. 用户点击升级按钮
2. 调用后端API获取Stripe checkout URL
3. 跳转到Stripe页面进行付款
4. 采用订阅方式，支持定期扣费

#### 计划配置

```javascript
const PLAN_CONFIG = {
  PRO: {
    name: 'Pro',
    price: 29,
    credits: 1000,
    icon: <Zap />,
    color: 'bg-blue-500',
  },
  ULTRA: {
    name: 'Ultra',
    price: 99,
    credits: 5000,
    icon: <Crown />,
    color: 'bg-purple-500',
  },
}
```

### 3. 取消订阅功能

#### 取消流程

1. 用户点击 "Cancel Subscription" 按钮
2. 显示确认对话框
3. 调用后端API取消订阅
4. 显示成功/失败提示
5. 刷新订阅状态

#### 安全措施

- 使用确认对话框防止误操作
- 显示操作状态（Cancelling...）
- 错误处理和用户反馈

### 4. 使用记录Table

#### 表格列

- **Date**: 使用日期
- **Prompt**: 提示词（前20字符，超出显示...）
- **Images**: 生成的图片数量
- **Size**: 图片尺寸比例
- **Credits Used**: 消耗的credit数量

#### 提示词处理

- 默认显示前20个字符
- 超出部分用 "..." 表示
- 鼠标悬停显示完整提示词（使用Tooltip组件）

#### 分页功能

- 支持10/20/50条记录每页
- 智能分页导航（显示当前页附近的页码）
- 首页、上一页、下一页、末页按钮
- 显示当前记录范围和总记录数

### 5. 数据获取

#### API调用

- `getUserCredits()`: 获取用户credit信息
- `getSubscriptionPlans()`: 获取订阅计划
- `getSubscriptions()`: 获取用户订阅状态
- `getUserCreditTransactions()`: 获取交易记录（支持分页）
- `getStripeCheckoutUrl()`: 获取Stripe支付链接
- `cancelSubscription()`: 取消订阅

#### 状态管理

- 使用React Query进行数据获取和缓存
- 使用Zustand管理用户状态
- 实时更新credit信息和订阅状态

### 6. 用户体验

#### 响应式设计

- 适配不同屏幕尺寸
- 移动端友好的按钮布局
- 合理的间距和字体大小

#### 交互反馈

- Loading状态显示
- 成功/错误提示
- 操作确认对话框
- 实时状态更新

#### 视觉层次

- 清晰的信息分组
- 一致的颜色主题
- 直观的图标使用
- 合理的留白和间距

## 技术实现

### 组件结构

```tsx
<Layout>
  <LayoutBody>
    {/* 页面标题 */}
    <div>Billing & Usage</div>

    {/* 顶部Card */}
    <Card>
      <CardHeader>{/* Credit信息和按钮 */}</CardHeader>
    </Card>

    {/* 交易记录Table */}
    <Card>
      <CardHeader>
        <CardTitle>Usage History</CardTitle>
      </CardHeader>
      <CardContent>
        {/* 分页控制 */}
        {/* Table */}
        {/* 分页导航 */}
      </CardContent>
    </Card>
  </LayoutBody>
</Layout>
```

### 状态管理

- `currentPage`: 当前页码
- `pageSize`: 每页记录数
- `creditInfo`: 用户credit信息
- `subscriptionsData`: 订阅数据
- `transactionsData`: 交易记录数据

### 错误处理

- API调用失败的用户提示
- 网络错误的友好提示
- 操作失败的详细说明
- 加载状态的用户反馈

## 使用说明

### 访问页面

- 通过侧边栏的 "Billing" 菜单项访问
- 或通过用户下拉菜单的 "Billing" 选项访问

### 升级计划

1. 在顶部Card中点击相应的升级按钮
2. 系统会跳转到Stripe支付页面
3. 完成支付后自动升级到对应计划

### 取消订阅

1. 点击 "Cancel Subscription" 按钮
2. 在确认对话框中确认操作
3. 系统会取消当前订阅

### 查看使用记录

1. 在底部的Table中查看所有使用记录
2. 使用分页控制浏览更多记录
3. 鼠标悬停在提示词上查看完整内容

## 注意事项

1. **权限控制**: 只有登录用户才能访问此页面
2. **数据安全**: 敏感操作需要用户确认
3. **实时更新**: 操作完成后会自动刷新相关数据
4. **错误处理**: 网络错误和API错误都有相应的用户提示
5. **响应式**: 页面在不同设备上都有良好的显示效果

## 未来扩展

1. **导出功能**: 支持导出使用记录为CSV/PDF
2. **筛选功能**: 按日期、类型等条件筛选记录
3. **图表统计**: 显示使用趋势和统计图表
4. **通知设置**: 订阅到期提醒和credit不足警告
5. **批量操作**: 支持批量管理订阅和记录
