import { authApi } from '@/lib/api'

export async function fileUpload() {
  return authApi.post('/files/upload')
}
