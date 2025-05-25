<script setup lang="ts">
import mapboxgl from "mapbox-gl";
import { onMounted, ref, watch } from "vue";
import { useBuildingStore } from "~/stores/building";
import ToiletDrawer from "./ToiletDrawer.vue";
import { useLocationStore } from "~/stores/location";
import { useUserModalStore } from "~/stores/userModal";
import Profile from "@/components/TheHeader/Profile/index.vue";

const colorMode = useColorMode();
const buildingStore = useBuildingStore();
const locationStore = useLocationStore();
const userModal = useUserModalStore();
useShareLocation();

const mapContainer = ref<HTMLElement | null>(null);
const mapInstance = ref<mapboxgl.Map | null>(null);

const drawerOpen = ref(false);
const selectedBuilding = ref<{ name: string; toilets: any[] } | null>(null);

mapboxgl.accessToken =
  "pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng";

// ✅ 主題對應地圖樣式
const getMapStyle = () => {
  return colorMode.value === "dark"
    ? "mapbox://styles/mapbox/dark-v11"
    : "mapbox://styles/mapbox/streets-v12";
};

async function renderBuildingMarkers() {
  if (!mapInstance.value) return;

  buildingStore.buildings.forEach((building: any) => {
    const el = document.createElement("div");

    el.innerText = "🚻";

    // 判斷主題
    const isDarkMode = document.documentElement.classList.contains("dark");
    const borderColor = isDarkMode ? "#fff" : "#3b82f6";
    const hoverBorderColor = isDarkMode ? "#ffffff" : "#1d4ed8"; // 更明顯的對比色

    // 🧼 標準樣式（白底圓框）
    el.style.cssText = `
      font-size: 20px;
      background-color: white;
      color: black;
      border-radius: 50%;
      width: 36px;
      height: 36px;
      display: flex;
      justify-content: center;
      align-items: center;
      line-height: 1;
      padding: 4px;
      cursor: pointer;
      border: 2px solid ${borderColor};
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
      transition: border 0.2s ease, box-shadow 0.2s ease;
      user-select: none;
    `;

    // ✅ Hover: 邊框變色、陰影加深
    el.addEventListener("mouseenter", () => {
      el.style.border = `2px solid ${hoverBorderColor}`;
      el.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.3)";
    });

    el.addEventListener("mouseleave", () => {
      el.style.border = `2px solid ${borderColor}`;
      el.style.boxShadow = "0 2px 6px rgba(0, 0, 0, 0.2)";
    });

    el.title = building.name;

    el.addEventListener("click", async () => {
      const toiletsRes = await fetch(
        `https://toilet-api-347656239330.asia-east1.run.app/api/toilets/building/${building.id}`,
      );
      const toilets = await toiletsRes.json();

      selectedBuilding.value = {
        name: building.name,
        toilets,
      };
      drawerOpen.value = true;
    });

    new mapboxgl.Marker(el)
      .setLngLat([building.lng, building.lat])
      .addTo(mapInstance.value as unknown as mapboxgl.Map);
  });
}

watch(
  () => locationStore.panOnce,
  (flag) => {
    if (!flag || !mapInstance.value || !locationStore.hasPos) return;

    const { lng, lat } = locationStore.coords!;

    mapInstance.value.flyTo({
      center: [lng, lat],
      zoom: 17,
      essential: true,
    });

    locationStore.panOnce = false; // ↩️ 重置旗標
  },
);

const userMarker = ref<mapboxgl.Marker | null>(null);
// 監聽座標，建立 / 更新 Marker
watch(
  () => locationStore.coords,
  (pos) => {
    if (!mapInstance.value || !pos) return;

    // ① 已有 marker → 更新位置
    if (userMarker.value) {
      userMarker.value.setLngLat([pos.lng, pos.lat]);
      return;
    }

    // ② 沒有 marker → 建立一顆
    const el = document.createElement("div");
    el.className = "user-marker";
    el.style.cssText =
      "width:14px;height:14px;border-radius:50%;background:#10b981;border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,.3)";
    userMarker.value = new mapboxgl.Marker(el)
      .setLngLat([pos.lng, pos.lat])
      .addTo(mapInstance.value as unknown as mapboxgl.Map);
  },
  { immediate: true },
);

const routeStore = useRouteStore();
let routeLayerId = "route-layer";
let routeSourceId = "route-source";
watch(
  () => routeStore.routeGeoJSON,
  (geojson) => {
    if (!mapInstance.value) return;

    const map = mapInstance.value;

    // 清理先前圖層與來源
    if (map.getLayer(routeLayerId)) {
      map.removeLayer(routeLayerId);
    }
    if (map.getSource(routeSourceId)) {
      map.removeSource(routeSourceId);
    }

    if (geojson && geojson.features?.length > 0) {
      map.addSource(routeSourceId, {
        type: "geojson",
        data: geojson,
      });

      map.addLayer({
        id: routeLayerId,
        type: "line",
        source: routeSourceId,
        layout: {
          "line-join": "round",
          "line-cap": "round",
        },
        paint: {
          "line-color": "#1d4ed8",
          "line-width": 4,
        },
      });

      const feature = geojson.features[0];
      const type = feature.geometry.type;
      let coords: number[][] = [];

      if (type === "LineString") {
        coords = feature.geometry.coordinates;
      } else if (type === "MultiLineString") {
        coords = feature.geometry.coordinates[0];
      }

      if (coords.length > 0) {
        const lastCoord = coords[coords.length - 1];
        map.flyTo({
          center: [lastCoord[0], lastCoord[1]],
          zoom: 17,
          essential: true,
        });
      }
    }
  },
  { immediate: true },
);

// ✅ 初始化地圖
onMounted(async () => {
  if (!mapContainer.value) return;

  const map = new mapboxgl.Map({
    container: mapContainer.value,
    style: getMapStyle(),
    center: [121.5773869, 24.9878484], // 政大
    zoom: 16,
  });

  map.addControl(new mapboxgl.NavigationControl());
  mapInstance.value = map;

  // 載入建築資料後渲染
  await buildingStore.fetchBuildings();
  renderBuildingMarkers();
});

watch(
  () => buildingStore.buildings,
  () => {
    renderBuildingMarkers();
  },
  { deep: true },
);

// ✅ 主題切換時更新 style
watch(colorMode, () => {
  if (mapInstance.value) {
    mapInstance.value.setStyle(getMapStyle());
  }
});

const { others } = useShareLocation();
const otherMarkers = ref<Record<string, mapboxgl.Marker>>({});

// 監聽 others 資料
watch(
  () => ({ ...others }), // ✅ 確保觸發變化偵測
  (updated) => {
    if (!mapInstance.value) return;

    // 移除舊的 Marker
    for (const marker of Object.values(otherMarkers.value)) {
      marker.remove();
    }
    otherMarkers.value = {};

    // 建立新的 Marker
    Object.entries(updated).forEach(([user_id, user]) => {
      const el = document.createElement("div");
      el.className = "other-user-marker";
      el.style.cssText = `
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background-image: url('${user.avatarUrl}');
        background-size: cover;
        background-position: center;
        border: 2px solid #3b82f6;
        box-shadow: 0 0 4px rgba(0,0,0,.3);
        cursor: pointer;
      `;
      el.title = user.name;

      el.addEventListener("click", () => {
        userModal.open(parseInt(user_id, 10));
      });

      const marker = new mapboxgl.Marker(el)
        .setLngLat([user.location.lng, user.location.lat])
        .addTo(mapInstance.value as unknown as mapboxgl.Map);

      otherMarkers.value[user_id] = marker;
    });
  },
  { deep: true, immediate: true },
);
</script>

<template>
  <ToiletDrawer
    v-if="selectedBuilding"
    v-model:open="drawerOpen"
    :isOpen="drawerOpen"
    :overlay="false"
    :buildingName="selectedBuilding.name"
    :toilets="selectedBuilding.toilets"
    @close="drawerOpen = false"
  />

  <UModal v-model:open="userModal.isOpen">
    <template #content>
      <Profile
        :userId="userModal.userId?.toString() || ''"
        @close="userModal.close()"
      />
    </template>
  </UModal>
  <div ref="mapContainer" class="w-full h-[calc(100vh-4rem)]" />
</template>
