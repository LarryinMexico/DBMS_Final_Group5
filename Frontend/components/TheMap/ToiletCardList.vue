<script setup lang="ts">
defineProps<{
  toilets: Array<{ floor: string | number; type: string; title?: string }>
}>()

const emit = defineEmits(['select'])
</script>

<template>
  <div class="space-y-3">
    <UCard
      v-for="(toilet, index) in toilets"
      :key="index"
      class="border border-gray-200 dark:border-gray-700 p-4"
      @click="emit('select', toilet)"
    >
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-base font-bold">
          {{ toilet.title || '無名稱' }}
          <span class="text-sm text-gray-400 ml-1">📍{{ toilet.floor }} 樓</span>
        </h3>
      </div>

      <div class="flex items-center space-x-4 text-sm text-red-500">
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-star-solid" />
          <span>5.0</span>
        </div>
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-chat-bubble-left-right" />
          <span>10 則</span>
        </div>
        <UButton
          label="我的最愛"
          color="error"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
        />
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 查無廁所資訊
    </p>
  </div>
</template>
