// stores/user.ts
export const useUserStore = defineStore("user", {
  state: () => ({
    id: null as number | null,
    name: "",
    email: "",
    avatar: "" as string | undefined,
    isAdmin: false,
  }),
  actions: {
    setUser(data: {
      id: number;
      name: string;
      email: string;
      avatar?: string;
      isAdmin?: boolean;
    }) {
      this.id = data.id;
      this.name = data.name;
      this.email = data.email;
      this.avatar = data.avatar;
      this.isAdmin = data.isAdmin ?? false;
    },
    clearUser() {
      this.id = null;
      this.name = "";
      this.email = "";
      this.avatar = undefined;
      this.isAdmin = false;
    },
  },
});
