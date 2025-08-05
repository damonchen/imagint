import { set } from 'lodash'
import { create } from 'zustand'

const useAccountStore = create((set) => ({
  account: {},
  setAccount: (account) => set(({ account }),
}))

export { useAccountStore }
