// composables/useSocket.ts
import { io } from "socket.io-client";
import { useUserStore } from "@/stores/user";
import { useToast } from "#imports";
import { BASE_URL } from "~/constants";
import { useUserModalStore } from "@/stores/userModal";

const socket = io(BASE_URL.replace("/api", ""), {
  transports: ["websocket"], // 建議避免 polling
  withCredentials: true,
});

let hasRegisteredListeners = false;

export const useSocket = () => {
  const userStore = useUserStore();
  const userModal = useUserModalStore();
  const toast = useToast();

  const joinRoom = () => {
    if (userStore.id) {
      socket.emit("join", { room: String(userStore.id) });
    }
  };

  const registerListeners = () => {
    if (hasRegisteredListeners) return; // ❌ 防呆：只綁一次
    hasRegisteredListeners = true;

    socket.on("connect", () => {
      joinRoom(); // 🚀 自動加入自己的房間
    });

    socket.on("comment-received", async (payload) => {
      const { toiletId, user, comment, rating } = payload;
      if (user === userStore.id) return; // 🙅‍♂️ 不要對自己彈出 toast

      // 🚀 1. 同時查詢廁所名稱與使用者資料
      const [toiletRes, userRes] = await Promise.all([
        fetch(`${BASE_URL}/toilets/${toiletId}`),
        fetch(`${BASE_URL}/users/${user}`),
      ]);

      const toilet = await toiletRes.json();
      const userInfo = await userRes.json();

      // 🏅 2. 根據評分設計不同 toast 樣式
      const ratingText =
        ["★ 超慘", "★★ 不推", "★★★ 普通", "★★★★ 推薦", "★★★★★ 神廁所"][
          rating - 1
        ] ?? "";

      toast.add({
        title: `${userInfo.name} 評論了「${toilet.title}」`,
        description: `${ratingText}：${comment}`,
        avatar: {
          src: userInfo.avatarUrl,
          alt: userInfo.name,
        },
        actions: [
          {
            label: "查看個人頁",
            color: "neutral",
            variant: "soft",
            icon: "i-heroicons-user-circle",
            onClick: (e) => {
              e?.stopPropagation();
              userModal.open(user);
            },
          },
        ],
      });
    });

    socket.on("disconnect", () => {
      console.warn("❌ Socket disconnected");
    });
  };

  registerListeners();

  return {
    socket,
    joinRoom,
  };
};
