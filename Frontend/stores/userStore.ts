// stores/userStore.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null as number | null,
    name: '',
    email: '',
  }),
  actions: {
    setUser(data: { id: number; name: string; email: string }) {
      this.id = data.id
      this.name = data.name
      this.email = data.email
    },
    clearUser() {
      this.id = null
      this.name = ''
      this.email = ''
    }
  }
})
