import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useToast } from "#imports";

interface Coord {
  lat: number;
  lng: number;
}

const GEO_TIMEOUT = 10_000; // 10秒 timeout
const CACHE_TTL = 60_000; // 1分鐘有效

export const useLocationStore = defineStore("location", () => {
  const toast = useToast();

  const coords = ref<Coord | null>(null);
  const lastFetched = ref(0);
  const watching = ref(false);
  const watchId = ref<number | null>(null);

  const panOnce = ref(false); // 將 `flyTo` 行為用 flag 控制
  const errorMsg = ref<string | null>(null);

  const hasPos = computed(() => coords.value !== null);

  /** ✅ 單次定位 */
  async function locate(force = false): Promise<Coord> {
    errorMsg.value = null;

    if (!force && coords.value && Date.now() - lastFetched.value < CACHE_TTL) {
      return coords.value;
    }

    if (!navigator.geolocation) {
      errorMsg.value = "此瀏覽器不支援定位功能";
      throw new Error(errorMsg.value);
    }

    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          coords.value = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
          };
          lastFetched.value = Date.now();
          resolve(coords.value);
        },
        (err) => {
          switch (err.code) {
            case 1:
              errorMsg.value = "請允許瀏覽器存取您的位置";
              break;
            case 2:
              errorMsg.value = "位置無法取得，請確認網路或 GPS 設定";
              break;
            case 3:
              errorMsg.value = "定位逾時，請再試一次";
              break;
            default:
              errorMsg.value = "定位失敗，請稍後再試";
          }

          toast.add({
            title: "📍 定位失敗",
            description: errorMsg.value,
            color: "error",
          });

          reject(new Error(errorMsg.value));
        },
        {
          enableHighAccuracy: true,
          timeout: GEO_TIMEOUT,
        },
      );
    });
  }

  /** ✅ 定位並設定 panOnce */
  async function locateAndRequestPan(force = false) {
    try {
      await locate(force);
      if (hasPos.value) panOnce.value = true;
    } catch (err) {
      // 錯誤訊息已在 locate 中處理過
    }
  }

  /** ✅ 啟用追蹤 */
  function startWatch() {
    if (watchId.value !== null || !navigator.geolocation) return;

    watchId.value = navigator.geolocation.watchPosition(
      (pos) => {
        coords.value = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        };
        lastFetched.value = Date.now();
      },
      (err) => {
        console.error("🔁 Watch error:", err);
      },
      {
        enableHighAccuracy: true,
        timeout: GEO_TIMEOUT,
        maximumAge: 0,
      },
    );

    watching.value = true;
  }

  /** ✅ 停止追蹤 */
  function stopWatch() {
    if (watchId.value !== null) {
      navigator.geolocation.clearWatch(watchId.value);
      watchId.value = null;
    }
    watching.value = false;
  }

  /** ✅ 切換追蹤狀態 */
  function toggleWatch() {
    watching.value ? stopWatch() : startWatch();
  }

  /** ✅ 當 flyTo 完畢後應該手動重置 */
  function ackPan() {
    panOnce.value = false;
  }

  return {
    coords,
    hasPos,
    panOnce,
    watching,
    errorMsg,
    locate,
    locateAndRequestPan,
    toggleWatch,
    ackPan,
  };
});
