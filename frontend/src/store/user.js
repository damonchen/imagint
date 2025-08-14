import { create } from 'zustand'

const useUserStore = create((set) => ({
  user: {},
  setUser: (user) => set({ user }),
  credit: {},
  setCredit: (credit) => set({ credit }),
}))

export { useUserStore }
