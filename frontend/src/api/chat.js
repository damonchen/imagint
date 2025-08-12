import { authApi } from '@/lib/api'

export async function createChat(prompt) {
  return authApi.post('/chats', {
    prompt,
  })
}

export async function getCurrentChat() {
  return authApi.get('/chats/current')
}

export async function getChatMessages(chatId) {
  return authApi.get(`/chats/${chatId}/messages`)
}

export async function createChatMessage(chatId, prompt, promptParams) {
  return authApi.post(`/chats/${chatId}/messages`, {
    prompt,
    params: promptParams,
  })
}

export async function getChatMessage(chatId, messageId) {
  return authApi.get(`/chats/${chatId}/messages/${messageId}`)
}

export async function getChats(page, pageSize) {
  return authApi.get('/chats', {
    params: {
      page,
      pageSize,
    },
  })
}
