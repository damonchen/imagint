import { appApi } from '@/lib/api'

export async function getPlans() {
  return appApi.get('/plans')
}

export async function payPlan(id) {
  return appApi.get(`/plans/${id}/pay`)
}

export async function getSubscriptions() {
  return appApi.get(`/subscriptions`)
}

export async function getSubscription(id) {
  return appApi.get(`/subscription/${id}`)
}

export async function getSubscriptionPayment(id) {
  return appApi.get(`/subscription/${id}/payment`)
}

export async function cancelTransaction(id) {
  return appApi.get(`/transaction/${id}/cancel`)
}

export async function refundTransaction(id) {
  return appApi.get(`/transaction/${id}/refund`)
}

export async function successTransaction(id) {
  return appApi.get(`/transaction/${id}/success`)
}

export async function failTransaction(id) {
  return appApi.get(`/transaction/${id}/fail`)
}

export async function startTransaction(id) {
  return appApi.get(`/transaction/${id}/start`)
}
