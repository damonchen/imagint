import { authApi } from '@/lib/api'

export async function getPlans() {
  return authApi.get('/plans')
}

export async function payPlan(id) {
  return authApi.get(`/plans/${id}/pay`)
}

export async function getSubscriptions() {
  return authApi.get(`/subscriptions`)
}

export async function getSubscription(id) {
  return authApi.get(`/subscription/${id}`)
}

export async function getSubscriptionPayment(id) {
  return authApi.get(`/subscription/${id}/payment`)
}

export async function cancelTransaction(id) {
  return authApi.get(`/transaction/${id}/cancel`)
}

export async function refundTransaction(id) {
  return authApi.get(`/transaction/${id}/refund`)
}

export async function successTransaction(id) {
  return authApi.get(`/transaction/${id}/success`)
}

export async function failTransaction(id) {
  return authApi.get(`/transaction/${id}/fail`)
}

export async function startTransaction(id) {
  return authApi.get(`/transaction/${id}/start`)
}

// 新增的API函数
export async function createSubscription(plan) {
  return authApi.post('/subscriptions', { ...plan })
}

export async function cancelSubscription(subscriptionId) {
  return authApi.post(`/subscriptions/${subscriptionId}/cancel`)
}

export async function getStripeCheckoutUrl(planId) {
  return authApi.post('/stripe/checkout', { planId })
}

export async function getPlan(planName) {
  return authApi.get(`/plan/${planName}`)
}
