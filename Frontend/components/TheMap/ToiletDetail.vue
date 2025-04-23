<script setup lang="ts">
const props = defineProps<{
  toilet: { id: string; floor: string | number; type: string; title?: string }
}>()
const emit = defineEmits(['back'])
</script>

<template>
  <div class="space-y-2">
    <p>WIP</p>
  </div>
</template>
