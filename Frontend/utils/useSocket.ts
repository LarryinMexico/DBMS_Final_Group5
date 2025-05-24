// composables/useSocket.ts
import { io } from "socket.io-client";
import { useUserStore } from "@/stores/user";
import { BASE_URL } from "~/constants";


const socket = io(BASE_URL.replace("/api",""), {
  transports: ["websocket"], // 建議避免 polling
  withCredentials: true,
});

export const useSocket = () => {
  const userStore = useUserStore();
  const toast = useToast();

  const joinRoom = () => {
    if (userStore.id) {
      socket.emit("join", { room: String(userStore.id) });
      console.log("📡 Join room:", userStore.id);
    }
  };

  // ✅ Socket 連線成功
socket.on("connect", () => {
  console.log("✅ Socket connected:", socket.id);
  toast.add({ title: "已連線到伺服器", description: `Socket ID: ${socket.id}`, color: "primary" });

  joinRoom(); // 🚀 自動加入自己的房間
});

  socket.on("disconnect", () => {
    console.warn("❌ Socket disconnected");
    toast.add({ title: "連線中斷", color: "warning" });
  });

  return {
    socket,
    joinRoom,
  };
};
