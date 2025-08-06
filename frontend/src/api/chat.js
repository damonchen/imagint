import { authApi } from '@/lib/api'

export async function createChat(prompt) {
  return authApi.post('/chats', {
    prompt,
  })
}

export async function createChatMessage(chatId, prompt, promptParams) {
  return authApi.post(`/chats/${chatId}/messages`, {
    prompt,
    promptParams,
  })
}

export async function getChatMessage(chatId, messageId) {
  return authApi.get(`/chats/${chatId}/messages/${messageId}`)
}
