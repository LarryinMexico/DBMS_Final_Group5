<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useReviews } from '@/utils/useReviews'
import { BASE_URL } from '@/constants'

const props = defineProps<{ toiletId: number, reload: number }>()

const {
  reviews,
  userInfoMap,
  hasReacted,
  reactionCount,
  toggleReaction,
  fetchReviews
} = useReviews(props.toiletId)

const toast = useToast()

onMounted(fetchReviews)

const showEditModal = ref(false)
const editComment = ref('')
const editRating = ref(0)
const editingId = ref<number | null>(null)


const startEdit = (reviewId: number) => {
  const review = reviews.value.find(r => r.id === reviewId)
  if (!review) return
  editingId.value = review.id
  editComment.value = review.comment
  editRating.value = review.rating
  showEditModal.value = true
  console.log('開始編輯評論', review)
}

const confirmEdit = async () => {
  if (!editingId.value) return
  try {
    const res = await fetch(`${BASE_URL}/reviews/${editingId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        comment: editComment.value,
        rating: editRating.value
      })
    })
    if (!res.ok) throw new Error('更新失敗')
    toast.add({ title: '評論已更新', color: 'success' })
    showEditModal.value = false
    await fetchReviews()
  } catch (err) {
    toast.add({ title: '評論更新失敗', color: 'error' })
  }
}

const deleteReview = async (reviewId: number) => {
  if (!confirm('確定要刪除這則評論嗎？')) return
  try {
    const res = await fetch(`${BASE_URL}/reviews/${reviewId}`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('刪除失敗')
    toast.add({ title: '已刪除評論', color: 'success' })
    await fetchReviews()
  } catch (err) {
    toast.add({ title: '刪除失敗', color: 'error' })
  }
}

watch(() => props.reload, fetchReviews)
</script>

<template>
  <div class="space-y-3 mt-4">
    <div
      v-for="review in reviews"
      :key="review.id"
      class="flex items-start space-x-3"
    >
      <UAvatar size="sm" :src="userInfoMap[review.user_id]?.avatarUrl" />

      <div class="flex flex-col w-full">
        <div class="flex items-center justify-between">
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

          <div class="flex items-center space-x-1">
            <UDropdownMenu
              v-if="review.isOwner"
              :items="[
                {
                  label: '編輯',
                  icon: 'i-heroicons-pencil-square',
                  onSelect: () => startEdit(review.id)
                },
                {
                  label: '刪除',
                  icon: 'i-heroicons-trash',
                  color: 'error',
                  onSelect: () => deleteReview(review.id)
                }
              ]"
              :popper="{ placement: 'bottom-end' }"
            >
              <UButton icon="i-heroicons-ellipsis-horizontal" color="neutral" variant="ghost" />
            </UDropdownMenu>

            <UButton
              icon="i-heroicons-heart"
              :variant="hasReacted(review.id) ? 'solid' : 'ghost'"
              color="error"
              @click="toggleReaction(review.id)"
              :disabled="review.isOwner"
            >
              <span class="text-sm">{{ reactionCount(review.id) }}</span>
            </UButton>
          </div>
        </div>

        <p class="text-sm text-gray-600 mt-1">
          {{ review.comment || '無評論內容' }}
        </p>

        <p class="text-xs text-gray-400 mt-1">{{ review.updateAt }}</p>
      </div>
    </div>

    <!-- 編輯評論 Modal -->
    <UModal v-model:open="showEditModal">
        <template #content>
      <div class="p-4 space-y-3">
        <h2 class="text-lg font-bold">編輯評論</h2>
        <UTextarea
          v-model="editComment"
          placeholder="更新你的評論內容"
          :maxrows="4"
          autoresize
        />
        <div class="flex items-center space-x-1">
          <UIcon
            v-for="n in 5"
            :key="n"
            name="i-heroicons-star-solid"
            class="w-6 h-6 cursor-pointer"
            :class="n <= editRating ? 'text-yellow-400' : 'text-gray-300'"
            @click="editRating = n"
          />
        </div>
        <div class="flex justify-end">
          <UButton label="儲存變更" color="primary" @click="confirmEdit" />
        </div>
      </div>
    </template>
    </UModal>
  </div>
</template>