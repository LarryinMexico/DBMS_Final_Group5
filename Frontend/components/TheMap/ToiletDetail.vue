<script setup lang="ts">
import { BASE_URL } from '@/constants'
import { useUserStore } from '@/stores/userStore'

const props = defineProps<{
  toilet: { id: number; floor: string | number; type: string; title?: string }
}>()

const rating = ref(0)
const comment = ref('') // 先備好
const user = useUserStore()
const toast = useToast()
const icons = Array.from({ length: 5 }, (_, i) => i + 1)

const submitReview = async () => {
  if (!user.id || rating.value === 0) return

  try {
    const res = await fetch(`${BASE_URL}/reviews/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: user.id,
        toilet_id: props.toilet.id,
        rating: rating.value
        // comment 未送出
      })
    })

    if (!res.ok) throw new Error('評論送出失敗')

    const result = await res.json()
    console.log('✅ 評論送出成功', result)

    toast.add({ title: '評論送出成功', color: 'success' })
    rating.value = 0
    comment.value = ''
  } catch (error) {
    toast.add({ title: '評論送出失敗', description: '請稍後再試', color: 'error' })
  }
  await fetchReviews() // POST 成功後立即重新拉取評論
}

const reviews = ref<{ user_id: number; rating: number; review_id: number }[]>([])

const userInfoMap = ref<Record<number, { name: string; avatarUrl: string }>>({})

const fetchUserInfo = async (userId: number) => {
  if (userInfoMap.value[userId]) return
  try {
    const res = await fetch(`${BASE_URL}/users/${userId}`)
    const data = await res.json()
    userInfoMap.value[userId] = {
      name: data.name,
      avatarUrl: data.avatarUrl
    }
  } catch (err) {
    console.warn(`❌ 無法取得使用者 ${userId} 資訊`, err)
  }
}

const fetchReviews = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/toilet/${props.toilet.id}`)
    if (!res.ok) throw new Error('無法取得評論')
    const fetched = await res.json()
    reviews.value = fetched
    for (const review of fetched) {
      fetchUserInfo(review.user_id)
    }
  } catch (err) {
    console.error('❌ 評論載入失敗', err)
  }
}

onMounted(fetchReviews)
</script>


<template>
  <div class="space-y-4">
    <!-- 使用者資訊 -->
    <div class="flex items-center space-x-3">
      <UAvatar size="md" :src="user.avatar" />
      <div>
        <p class="text-base font-bold">{{ user.name }}</p>
        <p class="text-xs text-gray-400">正在撰寫公開評論</p>
      </div>

    <!-- 評分區塊 -->
      <UIcon
        v-for="n in icons"
        :key="n"
        name="i-heroicons-star-solid"
        class="w-6 h-6 cursor-pointer transition-colors"
        :class="n <= rating ? 'text-yellow-400' : 'text-gray-400 hover:text-yellow-300'"
        @click="rating = n"
      />
    </div>

    <!-- 評論輸入 -->
    <UTextarea
      v-model="comment"
      :maxrows="4"
      :autoresize="true"
      placeholder="詳細說明你在這個地點的親身體驗"
      class="w-full"
    />

    <!-- 送出按鈕 -->
    <div class="flex justify-end">
      <UButton
        label="送出評論"
        color="primary"
        size="sm"
        :disabled="!comment || rating === 0"
        @click="submitReview"
      />
    </div>
  </div>

  <div class="space-y-3 mt-4">
    <div v-for="review in reviews" :key="review.review_id" class="flex items-start space-x-3">
      <UAvatar size="sm" :src="userInfoMap[review.user_id]?.avatarUrl" />
      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <p class="text-sm font-semibold">
            {{ userInfoMap[review.user_id]?.name || `使用者 ${review.user_id}` }}
          </p>
          <div class="flex items-center space-x-1 text-yellow-500">
            <UIcon
              v-for="n in 5"
              :key="n"
              :name="n <= review.rating ? 'i-heroicons-star-solid' : 'i-heroicons-star'"
              class="w-4 h-4"
            />
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-1">
          {{ '（尚無評論內容）' }}
        </p>
      </div>
    </div>

  </div>
</template>
