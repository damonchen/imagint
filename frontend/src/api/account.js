import { authApi } from '@/lib/api'

export async function getAccounts() {
  return authApi.get('/accounts')
}

export async function getAccount(id) {
  return authApi.post(`/accounts/${id}`)
}

export async function createAccount(data) {
  return authApi.post(`/accounts`, data)
}

export async function getAccountEmployees() {
  return authApi.put(`/accounts/employees`)
}

export async function getAccountCompnaies() {
  return authApi.get(`/accounts/companies`)
}

export async function resignAccount(id) {
  return authApi.put(`/accounts/${id}/resign`)
}

export async function selfResignAccount() {
  return authApi.post(`/self/resign`)
}

export async function getAddresses() {
  return authApi.get('/addresses')
}

export async function addAddress(address) {
  return authApi.post('/addresses', { address })
}

export async function getAddress(id) {
  return authApi.get(`/addresses/${id}`)
}

export async function getSelf() {
  return authApi.get('/self')
}
