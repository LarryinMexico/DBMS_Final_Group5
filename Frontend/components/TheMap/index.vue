<script setup lang="ts">
import mapboxgl from 'mapbox-gl'
import { onMounted, ref, watch } from 'vue'
import { useBuildingStore } from '~/stores/building'
import ToiletDrawer from './ToiletDrawer.vue'

const colorMode = useColorMode()
const buildingStore = useBuildingStore()

const mapContainer = ref<HTMLElement | null>(null)
const mapInstance = ref<mapboxgl.Map | null>(null)

const drawerOpen = ref(false)
const selectedBuilding = ref<{ name: string; toilets: any[] } | null>(null)

mapboxgl.accessToken = 'pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng'

// ✅ 主題對應地圖樣式
const getMapStyle = () => {
  return colorMode.value === 'dark'
    ? 'mapbox://styles/mapbox/dark-v11'
    : 'mapbox://styles/mapbox/streets-v12'
}

async function renderBuildingMarkers() {
  if (!mapInstance.value) return

  buildingStore.buildings.forEach((building: any) => {
    const el = document.createElement('div')
    el.className = 'building-marker'
    el.style.width = '12px'
    el.style.height = '12px'
    el.style.backgroundColor = '#3b82f6'
    el.style.borderRadius = '50%'
    el.style.cursor = 'pointer'

    // 👇 在點擊時才去 fetch 廁所資料與打開 drawer
    el.addEventListener('click', async () => {
      console.log('clicked', building.name)
      const toiletsRes = await fetch(`https://toilet-api-347656239330.asia-east1.run.app/api/toilets/building/${building.id}`)
      const toilets = await toiletsRes.json()

      selectedBuilding.value = {
        name: building.name,
        toilets
      }
      drawerOpen.value = true
    })

    new mapboxgl.Marker(el)
      .setLngLat([building.lng, building.lat])
      .addTo(mapInstance.value! as any)
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
    <ToiletDrawer
    v-if="selectedBuilding"
    v-model:open="drawerOpen"
    :isOpen="drawerOpen"
    :overlay="false"
    :buildingName="selectedBuilding.name"
    :toilets="selectedBuilding.toilets"
    @close="drawerOpen = false"
  />
  <div ref="mapContainer" class="w-full h-[calc(100vh-4rem)]" />
</template>

<style scoped>
.building-marker {
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.25);
  cursor: pointer;
}
</style>