<script setup lang="ts">
import { useToast } from '#imports'
import { BASE_URL } from '@/constants/index.js'
import { useUserStore } from '@/stores/userStore.js'

defineProps<{
  toilets: Array<{ id: number; floor: string | number; type: string; title?: string }>
}>()

const emit = defineEmits(['select'])

const favorites = ref<Set<number>>(new Set())
const stats = ref<Record<number, { avg_rating: number; count: number }>>({})

const isLoading = ref(true)

const fetchFavorites = async () => {
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
}

const fetchStats = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/stats`)
    if (!res.ok) throw new Error('取得評論統計失敗')

    const data = await res.json()
    stats.value = Object.fromEntries(
      data.map((item: any) => [item.toilet_id, { avg_rating: item.avg_rating, count: item.count }])
    )
  } catch (err) {
    console.error('❌ 無法取得 stats', err)
  }
}

onMounted(async () => {
  await Promise.all([fetchFavorites(), fetchStats()])
  isLoading.value = false
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
          <span>
            {{
              stats[toilet.id]?.avg_rating
                ? stats[toilet.id].avg_rating.toFixed(1)
                : '尚無評分'
            }}
          </span>
        </div>
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-chat-bubble-left-right" />
          <span>{{ stats[toilet.id]?.count || 0 }} 則</span>
        </div>

        <UButton
          v-if="!isLoading"
          :label="favorites.has(toilet.id) ? '已加入' : '我的最愛'"
          :color="favorites.has(toilet.id) ? 'success' : 'error'"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
          @click.stop="toggleFavorite(toilet.id)"
        />

        <UButton
          v-else
          loading
          variant="soft"
          color="neutral"
          size="xs"
        />
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 查無廁所資訊
    </p>
  </div>
</template>