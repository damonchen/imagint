import { create } from 'zustand'

// 每一个message，中有一个prompt和n个image对象，每一个image对象，至少有两个参数，一个是缩略图，一个是正常样式的图

const useCurrentChatStore = create((set) => ({
  chat: {
    messages: [],
  },
  message: {},
  setChat: (chat) => set({ chat }),
  setMessage: (message) => set({ message }),
}))

const useChatStore = create((set) => ({
  chats: [],
  setChats: (chats) => set({ chats }),
}))

export { useChatStore, useCurrentChatStore }
