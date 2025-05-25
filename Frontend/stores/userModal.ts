// stores/userModal.ts
export const useUserModalStore = defineStore("userModal", {
  state: () => ({
    userId: null as number | null,
    isOpen: false,
  }),
  actions: {
    open(id: number) {
      this.userId = id;
      this.isOpen = true;
    },
    close() {
      this.userId = null;
      this.isOpen = false;
    },
  },
});
