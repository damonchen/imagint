import { authApi } from '@/lib/api'

export async function createChatImages(chatId, prompt, promptParams) {
  return authApi.post(`/chats/${chatId}`, {
    prompt,
    promptParams,
  })
}

export async function getChatImages(chatId, messageId) {
  return authApi.get(`/chats/${chatId}/messages/${messageId}`)
}
