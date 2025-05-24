<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useReviews } from "@/utils/useReviews";
import { BASE_URL } from "@/constants";
import Profile from "@/components/TheHeader/Profile/index.vue";

const props = defineProps<{ toiletId: number; reload: number }>();

const {
  reviews,
  userInfoMap,
  hasReacted,
  reactionCount,
  toggleReaction,
  fetchReviews,
} = useReviews(props.toiletId);

const toast = useToast();

onMounted(fetchReviews);

const showEditModal = ref(false);
const editComment = ref("");
const editRating = ref(0);
const editingId = ref<number | null>(null);

const startEdit = (reviewId: number) => {
  const review = reviews.value.find((r) => r.id === reviewId);
  if (!review) return;
  editingId.value = review.id;
  editComment.value = review.comment;
  editRating.value = review.rating;
  showEditModal.value = true;
  console.log("開始編輯評論", review);
};

const confirmEdit = async () => {
  if (!editingId.value) return;
  try {
    const res = await fetch(`${BASE_URL}/reviews/${editingId.value}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        comment: editComment.value,
        rating: editRating.value,
      }),
    });
    if (!res.ok) throw new Error("更新失敗");
    toast.add({ title: "評論已更新", color: "success" });
    showEditModal.value = false;
    await fetchReviews();
  } catch (err) {
    toast.add({ title: "評論更新失敗", color: "error" });
  }
};

const deleteReview = async (reviewId: number) => {
  if (!confirm("確定要刪除這則評論嗎？")) return;
  try {
    const res = await fetch(`${BASE_URL}/reviews/${reviewId}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error("刪除失敗");
    toast.add({ title: "已刪除評論", color: "success" });
    await fetchReviews();
  } catch (err) {
    toast.add({ title: "刪除失敗", color: "error" });
  }
};

watch(() => props.reload, fetchReviews);

const sortKey = ref<"time" | "rating" | "popularity">("time");
const sortOrder = ref<"asc" | "desc">("desc");

const sortedReviews = computed(() => {
  const sorted = [...reviews.value].sort((a, b) => {
    let result = 0;

    if (sortKey.value === "time") {
      result = new Date(a.updateAt).getTime() - new Date(b.updateAt).getTime();
    } else if (sortKey.value === "rating") {
      result = a.rating - b.rating;
    } else if (sortKey.value === "popularity") {
      result = reactionCount(a.id) - reactionCount(b.id); // 多的在前（先設為 desc）
    }

    return sortOrder.value === "asc" ? result : -result;
  });
  return sorted;
});

const selectedUserId = ref<number | null>(null);
const showUserModal = ref(false);

const openUserModal = (userId: number) => {
  selectedUserId.value = userId;
  showUserModal.value = true;
};

</script>

<template>
  <div v-if="reviews.length === 0" class="text-sm text-gray-500 mt-4">
    <p>目前沒有評論</p>
    <p>快來成為第一位評論者吧！</p>
    <p>點擊上方按鈕來新增評論</p>
  </div>
  <div v-else class="space-y-3 mt-4">
    <!-- 排序按鈕區 -->
    <div class="flex justify-between items-center gap-2 mb-2">
      <!-- 排序條件切換（時間 / 評分） -->
      <UButtonGroup size="sm">
        <UButton
          :variant="sortKey === 'time' ? 'solid' : 'ghost'"
          @click="sortKey = 'time'"
          icon="i-heroicons-clock"
          label="時間"
        />
        <UButton
          :variant="sortKey === 'rating' ? 'solid' : 'ghost'"
          @click="sortKey = 'rating'"
          icon="i-heroicons-star"
          label="評分"
        />
        <UButton
          :variant="sortKey === 'popularity' ? 'solid' : 'ghost'"
          @click="sortKey = 'popularity'"
          label="熱門"
          icon="i-heroicons-fire"
          size="sm"
        />
      </UButtonGroup>

      <!-- 排序方向切換（遞增 / 遞減） -->
      <UButton
        :label="sortOrder === 'asc' ? '低到高' : '高到低'"
        size="sm"
        @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
        :icon="
          sortOrder === 'asc' ? 'i-lucide-arrow-down' : 'i-lucide-arrow-up'
        "
        variant="ghost"
      />
    </div>

    <div
      v-for="review in sortedReviews"
      :key="review.id"
      class="flex items-start space-x-3"
    >
      <UAvatar
        size="sm"
        :src="userInfoMap[review.user_id]?.avatarUrl"
        class="mt-3"
        @click="openUserModal(review.user_id)"
      />

      <div class="flex flex-col w-full">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <p class="text-sm font-semibold">
              {{
                userInfoMap[review.user_id]?.name || `使用者 ${review.user_id}`
              }}
            </p>
            <div class="flex items-center space-x-1 text-yellow-500">
              <UIcon
                v-for="n in 5"
                :key="n"
                :name="
                  n <= review.rating
                    ? 'i-heroicons-star-solid'
                    : 'i-heroicons-star'
                "
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
                  onSelect: () => startEdit(review.id),
                },
                {
                  label: '刪除',
                  icon: 'i-heroicons-trash',
                  color: 'error',
                  onSelect: () => deleteReview(review.id),
                },
              ]"
              :popper="{ placement: 'bottom-end' }"
            >
              <UButton
                icon="i-heroicons-ellipsis-horizontal"
                color="neutral"
                variant="ghost"
              />
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
          {{ review.comment || "無評論內容" }}
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

    <UModal v-model:open="showUserModal">
      <template #content>
        <Profile
          :userId="selectedUserId?.toString() || ''"
          @close="showUserModal = false"
          />
      </template>
    </UModal>
  </div>
</template>
