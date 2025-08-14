import { authApi } from '@/lib/api'

export async function getUserCredits() {
  const response = await authApi.get('/user/credits')
  return response
}

export async function getSubscriptionPlans() {
  const response = await authApi.get('/subscription/plans')
  return response
}

export async function getUserCreditTransactions(page = 1, perPage = 20) {
  const response = await authApi.get(
    `/user/credits/transactions?page=${page}&per_page=${perPage}`
  )
  return response
}
