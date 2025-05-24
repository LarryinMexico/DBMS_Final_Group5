// v4 旗標 + 追蹤
import { defineStore } from "pinia";
import { ref, computed } from "vue";

interface Coord { lat: number; lng: number }
const GEO_TIMEOUT = 10_000;
const CACHE_TTL   = 60_000;

export const useLocationStore = defineStore("location", () => {
  /* state */
  const toast = useToast();
  const coords      = ref<Coord | null>(null);
  const lastFetched = ref(0);
  const panOnce   = ref(false);           // 只飛一次
  const watching    = ref(false);           // 追蹤中？
  const watchId     = ref<number | null>(null);
  const errorMsg      = ref<string | null>(null);  // ⚠️ 新增：錯誤訊息可供 UI 顯示
  const hasPos = computed(() => coords.value !== null);

  async function locate(force = false): Promise<Coord> {
    errorMsg.value = null; // 每次先清空

    if (!force && coords.value && Date.now() - lastFetched.value < CACHE_TTL)
      return coords.value;

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
        title: "定位失敗",
        description: errorMsg.value,
        color: "error",
      });
          reject(new Error(errorMsg.value));
        },
        { enableHighAccuracy: true, timeout: GEO_TIMEOUT },
      );
    });
  }

  async function locateAndRequestPan(force = false) {
    await locate(force).then(() => {
      if (hasPos.value) panOnce.value = true;
    }).catch(console.error); // 保留給 UI 顯示
  }

  /* ------- 追蹤 ------- */
  function startWatch() {
    if (watchId.value !== null || !navigator.geolocation) return;
    watchId.value = navigator.geolocation.watchPosition(
      (pos) => {
        coords.value = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        lastFetched.value = Date.now();
      },
      console.error,
      { enableHighAccuracy: true, maximumAge: 0, timeout: GEO_TIMEOUT },
    );
    watching.value = true;
  }

  function stopWatch() {
    if (watchId.value !== null) {
      navigator.geolocation.clearWatch(watchId.value);
      watchId.value = null;
    }
    watching.value = false;
  }

  function toggleWatch() {
    watching.value ? stopWatch() : startWatch();
  }

  /* Map.vue call after flyTo */
  function ackPan() { panOnce.value = false; }

  return {
    coords, hasPos, panOnce, watching, errorMsg,
    locateAndRequestPan, toggleWatch, ackPan,
  };
});
