import { create } from 'zustand'

// 每一个message，中有一个prompt和n个image对象，每一个image对象，至少有两个参数，一个是缩略图，一个是正常样式的图

const useChatStore = create((set) => ({
  chat: {
    messages: [],
  },
  setChat: (chat) => set({ chat }),
}))

export { useChatStore }
