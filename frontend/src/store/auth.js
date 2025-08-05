import { create } from 'zustand';

// 从local storage中获取token值

// const TokenDataSchema = z.object({
//   userId: z.string(),
//   roles,
// });

const useAuthStore = create((set) => ({
  accessToken: '',
  refreshToken: '',
  setToken: (token) =>
    set({
      token: token,
    }),
  clearToken: () => {
    set({ token: '' });
  },
}));

export { useAuthStore };
