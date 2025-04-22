<script setup lang="ts">
const props = defineProps<{
  toilet: { id: string; floor: string | number; type: string; title?: string }
}>()
const emit = defineEmits(['back'])
</script>

<template>
  <div class="space-y-2">
    <UButton icon="i-lucide-chevron-left" variant="ghost" @click="emit('back')" label="返回" />
    <h3 class="text-xl font-bold">{{ toilet.title || '無名稱' }}</h3>
    <p class="text-sm">樓層：{{ toilet.floor }}</p>
    <p class="text-sm">類型：{{ toilet.type }}</p>
    <!-- 可加上評論 / 收藏 / icon 等 -->
  </div>
</template>
