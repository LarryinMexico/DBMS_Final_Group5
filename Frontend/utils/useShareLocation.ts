// composables/useShareLocation.ts
import { io } from "socket.io-client";
import { watch, ref, reactive } from "vue";
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/user";
import { useLocationStore } from "@/stores/location";

const socket = io(BASE_URL.replace("/api", ""), {
  transports: ["websocket"],
  withCredentials: true,
});

export const useShareLocation = () => {
  const user = useUserStore();
  const locationStore = useLocationStore();

  const othersLocation = reactive<Record<string, { lat: number; lng: number }>>({});
  const isSharing = ref(false);
  let shareInterval: ReturnType<typeof setInterval> | null = null;

  // 自動偵測是否啟動分享
  watch(
    () => locationStore.hasPos,
    (hasPos) => {
      if (hasPos && !isSharing.value && user.id) {
        isSharing.value = true;
        shareInterval = setInterval(() => {
          if (!locationStore.coords || !user.id) return;
          socket.emit("update-location", {
            user_id: user.id,
            lat: locationStore.coords.lat,
            lng: locationStore.coords.lng,
          });
        }, 5000);
      }

      if (!hasPos && shareInterval) {
        clearInterval(shareInterval);
        shareInterval = null;
        isSharing.value = false;
      }
    },
    { immediate: true },
  );

  // 接收他人位置
  socket.on("location-updated", ({ user_id, location }) => {
    if (user_id === user.id) return;
    othersLocation[user_id] = location;
  });

  return {
    isSharing,
    othersLocation,
  };
};