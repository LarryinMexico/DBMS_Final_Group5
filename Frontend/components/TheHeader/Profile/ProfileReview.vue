<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { BASE_URL } from "@/constants";
import { useToiletDrawer } from "@/stores/useToiletDrawer";

interface FullReview {
  id: number;
  rating: number;
  comment: string;
  updateAt: string;
  toilet: {
    id: number;
    title: string;
  };
  user: {
    id: string;
    name: string;
    avatarUrl: string;
  };
  reactionsCount: number;
}

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  enableSort: {
    type: Boolean,
    default: true,
  },
  pageSize: {
    type: Number,
    default: 5,
  },
});

const enrichedReviews = ref<FullReview[]>([]);
const isLoading = ref(true);

const sortKey = ref<"time" | "rating">("time");
const sortOrder = ref<"asc" | "desc">("desc");
const currentPage = ref(1);
const drawerStore = useToiletDrawer();

onMounted(async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/user/${props.userId}/full`);
    if (!res.ok) throw new Error("取得 enriched reviews 失敗");
    enrichedReviews.value = await res.json();
  } catch (err) {
    console.error("❌ 載入 enriched reviews 發生錯誤", err);
  } finally {
    isLoading.value = false;
  }
});

const sortedReviews = computed(() => {
  return [...enrichedReviews.value].sort((a, b) => {
    const aVal =
      sortKey.value === "time" ? new Date(a.updateAt).getTime() : a.rating;
    const bVal =
      sortKey.value === "time" ? new Date(b.updateAt).getTime() : b.rating;
    return sortOrder.value === "asc" ? aVal - bVal : bVal - aVal;
  });
});

const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * props.pageSize;
  return sortedReviews.value.slice(start, start + props.pageSize);
});
</script>

<template>
  <div class="space-y-3">
    <div v-if="enableSort" class="flex justify-between items-center gap-2 mb-2">
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
      </UButtonGroup>

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

    <div v-if="isLoading" class="text-center">📦 載入中...</div>

    <div
      v-for="review in paginatedReviews"
      :key="review.id"
      @click="drawerStore.open(review.toilet.id)"
      class="cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg p-2 transition"
    >
      <div class="flex items-start space-x-3">
        <UAvatar size="sm" class="mt-3" :src="review.user.avatarUrl" />

        <div class="flex flex-col w-full">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              {{ review.user.name }}
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
              <span class="text-xs text-gray-400"
                >@ {{ review.toilet.title }}</span
              >
            </div>

            <UButton
              icon="i-heroicons-heart"
              variant="ghost"
              color="error"
              :disabled="true"
            >
              <span class="text-sm">{{ review.reactionsCount }}</span>
            </UButton>
          </div>

          <p class="text-sm text-gray-600 mt-1">
            {{ review.comment || "無評論內容" }}
          </p>

          <div
            class="flex justify-between items-center text-xs text-gray-400 mt-1"
          >
            <span>{{ review.updateAt }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="pt-2 items-center flex justify-center">
      <UPagination
        v-if="sortedReviews.length > props.pageSize"
        v-model:page="currentPage"
        :itemsPerPage="props.pageSize"
        :total="sortedReviews.length"
      />
    </div>
  </div>
</template>
