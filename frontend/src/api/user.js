import { authApi } from '@/lib/api'

export async function getUsers() {
  return authApi.get('/users')
}

export async function getUser(id) {
  return authApi.post(`/users/${id}`)
}

export async function createUser(data) {
  return authApi.post(`/users`, data)
}

export async function getUserEmployees() {
  return authApi.put(`/users/employees`)
}

export async function getUserCompnaies() {
  return authApi.get(`/users/companies`)
}

export async function resignUser(id) {
  return authApi.put(`/users/${id}/resign`)
}

export async function selfResignUser() {
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

export async function changePassword(data) {
  return authApi.post('/self/change-password', data)
}

export async function updateProfile(data) {
  return authApi.post('/self/update-profile', data)
}

export async function updateAppearance(data) {
  return authApi.post('/self/appearance', data)
}
