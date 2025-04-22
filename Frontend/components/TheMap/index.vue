<script setup lang="ts">
import mapboxgl from 'mapbox-gl'
import { onMounted, ref, watch } from 'vue'
import { renderToString } from 'vue/server-renderer'
import { useBuildingStore } from '~/stores/building'
import ToiletTable from './ToiletTable.vue'

const colorMode = useColorMode()
const buildingStore = useBuildingStore()

const mapContainer = ref<HTMLElement | null>(null)
const mapInstance = ref<mapboxgl.Map | null>(null)

mapboxgl.accessToken = 'pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng'

// ✅ 主題對應地圖樣式
const getMapStyle = () => {
  return colorMode.value === 'dark'
    ? 'mapbox://styles/mapbox/dark-v11'
    : 'mapbox://styles/mapbox/streets-v12'
}

// ✅ 渲染建築 Marker
async function renderBuildingMarkers() {
  if (!mapInstance.value) return

  buildingStore.buildings.forEach(async (building: any) => {
    const el = document.createElement('div')
    el.className = 'building-marker'
    el.style.width = '12px'
    el.style.height = '12px'
    el.style.backgroundColor = '#3b82f6'
    el.style.borderRadius = '50%'

    // ✅ 取得該建築物的廁所資訊
    const toiletsRes = await fetch(`https://toilet-api-347656239330.asia-east1.run.app/api/toilets/building/${building.id}`)
    const toilets = await toiletsRes.json()

    // ✅ 渲染 Vue 元件為 HTML 字串
    const popupHtml = await renderToString(
      h(ToiletTable, {
        toilets,
        buildingName: building.name
      })
    )

    new mapboxgl.Marker(el)
      .setLngLat([building.lng, building.lat])
      .setPopup(new mapboxgl.Popup().setHTML(popupHtml))
      .addTo(mapInstance.value as any)
  })
}

// ✅ 初始化地圖
onMounted(async () => {
  if (!mapContainer.value) return

  const map = new mapboxgl.Map({
    container: mapContainer.value,
    style: getMapStyle(),
    center: [121.5773869, 24.9878484], // 政大
    zoom: 16
  })

  map.addControl(new mapboxgl.NavigationControl())
  mapInstance.value = map

  // 載入建築資料後渲染
  await buildingStore.fetchBuildings()
  renderBuildingMarkers()
})

watch(() => buildingStore.buildings, () => {
  renderBuildingMarkers()
}, { deep: true })

// ✅ 主題切換時更新 style
watch(colorMode, () => {
  if (mapInstance.value) {
    mapInstance.value.setStyle(getMapStyle())
  }
})
</script>

<template>
  <div ref="mapContainer" class="w-full h-[calc(100vh-4rem)]" />
</template>

<style scoped>
.building-marker {
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.25);
  cursor: pointer;
}
</style>