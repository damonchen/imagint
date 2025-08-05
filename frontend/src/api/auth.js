import { appApi } from '@/lib/api'

export async function signIn({ email, password }) {
  console.log('sigin in', import.meta.env.VITE_PUBLIC_API_URL)
  return await appApi.post('/auth/password/signin', { email, password })
}

export async function signUp({ email, password }) {
  return await appApi.post('/auth/password/signup', { email, password })
}

export async function resetPassword(email) {
  return await appApi.post('/auth/password/reset', { email })
}

export async function logout() {
  return await appApi.post('/auth/logout')
}

export async function captcha() {
  return await appApi.post('/auth/captcha')
}

export async function captchaVerify() {
  return await appApi.post('/auth/captcha/verify')
}
