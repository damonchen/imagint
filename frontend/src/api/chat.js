import { authApi } from '@/lib/api'

export async function createChat(prompt) {
  const response = await authApi.post('/chats', { prompt })
  return response
}

export async function getCurrentChat() {
  const response = await authApi.get('/chats/current')
  return response
}

export async function getChatMessages(chatId) {
  const response = await authApi.get(`/chats/${chatId}/messages`)
  return response
}

export async function createChatMessage(chatId, prompt, promptParams) {
  const response = await authApi.post(`/chats/${chatId}/messages`, {
    prompt,
    params: promptParams,
  })
  return response
}

export async function getChatMessage(chatId, messageId) {
  const response = await authApi.get(`/chats/${chatId}/messages/${messageId}`)
  return response
}

export async function getChats(page, pageSize) {
  const response = await authApi.get('/chats', {
    params: {
      page,
      pageSize,
    },
  })
  return response
}
