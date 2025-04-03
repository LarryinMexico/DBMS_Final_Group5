<script setup lang="ts">
import mapboxgl from 'mapbox-gl'
import { onMounted, ref, watch } from 'vue'

const colorMode = useColorMode()

const mapContainer = ref<HTMLElement | null>(null)
const mapInstance = ref<mapboxgl.Map | null>(null)

mapboxgl.accessToken = 'pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng'

// ✅ 根據主題取得對應 style URL
const getMapStyle = () => {
  return colorMode.value === 'dark'
    ? 'mapbox://styles/mapbox/dark-v11'
    : 'mapbox://styles/mapbox/streets-v12'
}

onMounted(() => {
  if (!mapContainer.value) return

  const map = new mapboxgl.Map({
    container: mapContainer.value,
    style: getMapStyle(),
    center: [121.5773869, 24.9878484], // 政大座標
    zoom: 16
  })

  map.addControl(new mapboxgl.NavigationControl())
  mapInstance.value = map
})

// ✅ 偵測主題切換，動態更換 map style
watch(colorMode, (newMode) => {
  if (mapInstance.value) {
    mapInstance.value.setStyle(getMapStyle())
  }
})
</script>

<template>
  <div ref="mapContainer" class="w-full h-[calc(100vh-4rem)]" />
</template>

<style scoped>
.mapboxgl-canvas {
  position: relative;
}
</style>
