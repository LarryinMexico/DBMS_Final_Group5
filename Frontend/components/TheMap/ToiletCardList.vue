<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '#imports'
import { BASE_URL } from '@/constants/index.js'
import { useUserStore } from '@/stores/userStore.js'

defineProps<{
  toilets: Array<{ id: number; floor: string | number; type: string; title?: string }>
}>()

const emit = defineEmits(['select'])

const favorites = ref<Set<number>>(new Set()) // 簡易紀錄收藏狀態

onMounted(async () => {
  const userId = userStore?.id
  if (!userId) return

  try {
    const res = await fetch(`${BASE_URL}/favorites/list/${userId}`)
    if (!res.ok) throw new Error('取得最愛失敗')

    const data = await res.json()
    const ids = data.map((item: { toilet_id: number }) => item.toilet_id)
    favorites.value = new Set(ids)
  } catch (error) {
    console.error('❌ 無法載入最愛列表', error)
  }
})

const userStore = useUserStore()

const toggleFavorite = async (toiletId: number) => {
  const userId = userStore?.id

  if (!userId) return

  const toast = useToast()

  const isFavorited = favorites.value.has(toiletId)
  const method = isFavorited ? 'DELETE' : 'POST'
  const endpoint = `${BASE_URL}/favorites/${isFavorited ? 'delete' : 'add'}`
  const payload = JSON.stringify({ user_id: userId, toilet_id: toiletId })

  const res = await fetch(endpoint, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: payload
  })

  if (res.ok) {
    if (isFavorited) {
      favorites.value.delete(toiletId)
      toast.add({ title: '已移除最愛', color: 'error' })
    } else {
      favorites.value.add(toiletId)
      toast.add({ title: '成功加入最愛', color: 'success' })
    }
  } else {
    toast.add({ title: '操作失敗', description: '請稍後再試', color: 'error' })
  }
}
</script>

<template>
  <div class="space-y-3">
    <UCard
      v-for="(toilet, index) in toilets"
      :key="index"
      class="border border-gray-200 dark:border-gray-700 p-4"
      @click.self="emit('select', toilet)"
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
          :label="favorites.has(toilet.id) ? '已加入' : '我的最愛'"
          :color="favorites.has(toilet.id) ? 'success' : 'error'"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
          @click.stop="toggleFavorite(toilet.id)"
        />
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 查無廁所資訊
    </p>
  </div>
</template>
