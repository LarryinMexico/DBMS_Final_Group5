// stores/userStore.ts
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    id: null as number | null,
    name: "",
    email: "",
    avatar: "" as string | undefined,
  }),
  actions: {
    setUser(data: {
      id: number;
      name: string;
      email: string;
      avatar?: string;
    }) {
      this.id = data.id;
      this.name = data.name;
      this.email = data.email;
      this.avatar = data.avatar;
    },
    clearUser() {
      this.id = null;
      this.name = "";
      this.email = "";
      this.avatar = undefined;
    },
  },
});
