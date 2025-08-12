import { create } from 'zustand'

// 每一个message，中有一个prompt和n个image对象，每一个image对象，至少有两个参数，一个是缩略图，一个是正常样式的图


export interface Image {
  id: number;
  imageUrl: string;
  thumbnailUrl: string;
  createdAt: string;
}


export interface Message {
  id: number;
  prompt: string;
  params: any;
  images: Image[];
  status: 'idle' | 'running' | 'success' | 'failed';
  count: number;
  type: 'text2image' | 'image2image' | 'text2video' | 'image2video';
  ratio: '1:1' | '16:9' | '4:3';
  model: 'qwen-image' | 'flux.dev' | 'stable-diffusion';
  size: '1:1' | '16:9' | '4:3';
  createdAt: string;
  updatedAt: string;
}

export interface Chat {
  id: number;
  messages: Message[];
}

const useCurrentChatStore = create((set) => ({
  chat: {
    messages: [],
  },
  message: {},
  setChat: (chat: Chat) => set({ chat }),
  setMessage: (message: Message) => set({ message }),
}))

const useChatStore = create((set) => ({
  chats: [],
  setChats: (chats: Chat[]) => set({ chats }),
}))

export { useChatStore, useCurrentChatStore }
