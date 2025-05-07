<script setup lang="ts">
import mapboxgl from "mapbox-gl";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({ lng: 121.5773869, lat: 24.9878484 }),
  },
});

const emit = defineEmits(["update:modelValue"]);

const mapContainer = ref<HTMLElement | null>(null);
const mapInstance = ref<mapboxgl.Map | null>(null);
const markerInstance = ref<mapboxgl.Marker | null>(null);

const colorMode = useColorMode();

mapboxgl.accessToken =
  "pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng";

const getMapStyle = () => {
  return colorMode.value === "dark"
    ? "mapbox://styles/mapbox/dark-v11"
    : "mapbox://styles/mapbox/streets-v12";
};

onMounted(() => {
  if (!mapContainer.value) return;

  const map = new mapboxgl.Map({
    container: mapContainer.value,
    style: getMapStyle(),
    center: [props.modelValue.lng, props.modelValue.lat],
    zoom: 17,
  });

  map.addControl(new mapboxgl.NavigationControl());

  const marker = new mapboxgl.Marker({ draggable: true })
    .setLngLat([props.modelValue.lng, props.modelValue.lat])
    .addTo(map);

  marker.on("dragend", () => {
    const lngLat = marker.getLngLat();
    emit("update:modelValue", { lng: lngLat.lng, lat: lngLat.lat });
  });

  map.on("click", (e) => {
    const lngLat = e.lngLat;
    marker.setLngLat(lngLat);
    emit("update:modelValue", { lng: lngLat.lng, lat: lngLat.lat });
  });

  mapInstance.value = map;
  markerInstance.value = marker;
});

watch(colorMode, () => {
  if (mapInstance.value) {
    mapInstance.value.setStyle(getMapStyle());
  }
});
</script>

<template>
  <div ref="mapContainer" class="w-full h-72 rounded overflow-hidden" />
</template>

<style scoped>
.mapboxgl-canvas {
  position: relative;
}
</style>
