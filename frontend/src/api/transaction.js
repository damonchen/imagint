import { authApi } from '@/lib/api'

export async function getSubscription() {
  return authApi.get(`/subscriptions`)
}
