import { authApi } from '@/lib/api'

export async function getProjects() {
  return authApi.get('/projects')
}

export async function getProject(id) {
  return authApi.get(`/projects/${id}`)
}
