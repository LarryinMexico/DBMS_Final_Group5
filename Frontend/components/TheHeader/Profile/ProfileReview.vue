<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { PropType } from "vue";
import { BASE_URL } from "@/constants";
import { useToiletDrawer } from "@/stores/useToiletDrawer";

interface Review {
  id: number;
  user_id: string;
  comment: string;
  rating: number;
  updateAt: string;
  toilet_id: number;
}

interface UserMap {
  [userId: string]: {
    name: string;
    avatarUrl: string;
  };
}

const props = defineProps({
  reviews: {
    type: Array as PropType<Review[]>,
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

const sortKey = ref<"time" | "rating">("time");
const sortOrder = ref<"asc" | "desc">("desc");
const currentPage = ref(1);

const reactionMap = ref<Record<number, number>>({});
const userInfoMap = ref<UserMap>({});
const toiletTitleMap = ref<Record<number, string>>({});
const drawerStore = useToiletDrawer();

const userInfo = ref<{ name: string; avatarUrl: string }>({
  name: "",
  avatarUrl: "",
});

const fetchReactionsAndToilets = async () => {
  const reactions: Record<number, number> = {};
  const titles: Record<number, string> = {};

  // ✅ 只抓一次 user
  const userRes = await fetch(`${BASE_URL}/users/${props.reviews[0].user_id}`);
  const userData = await userRes.json();
  userInfo.value = {
    name: userData.name,
    avatarUrl: userData.avatarUrl,
  };

  await Promise.all(
    props.reviews.map(async (review) => {
      try {
        const [reactionRes, toiletRes] = await Promise.all([
          fetch(`${BASE_URL}/reactions/review/${review.id}`),
          fetch(`${BASE_URL}/toilets/${review.toilet_id}`),
        ]);

        reactions[review.id] = (await reactionRes.json()).length || 0;

        const toiletData = await toiletRes.json();
        titles[review.toilet_id] =
          toiletData.title || `廁所 #${review.toilet_id}`;
      } catch {
        reactions[review.id] = 0;
      }
    }),
  );

  reactionMap.value = reactions;
  toiletTitleMap.value = titles;
};

onMounted(fetchReactionsAndToilets);

const sortedReviews = computed(() => {
  if (!Array.isArray(props.reviews)) return [];
  return [...props.reviews].sort((a, b) => {
    const result =
      sortKey.value === "time"
        ? new Date(a.updateAt).getTime() - new Date(b.updateAt).getTime()
        : a.rating - b.rating;
    return sortOrder.value === "asc" ? result : -result;
  });
});

const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * props.pageSize;
  const end = start + props.pageSize;
  return sortedReviews.value.slice(start, end);
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

    <div
      v-for="review in paginatedReviews"
      :key="review.id"
      @click="drawerStore.open(review.toilet_id)"
      class="cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg p-2 transition"
    >
      <div class="flex items-start space-x-3">
        <UAvatar size="sm" class="mt-3" :src="userInfo.avatarUrl" />

        <div class="flex flex-col w-full">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              {{ userInfo.name || `使用者 ${props.reviews[0].user_id}` }}
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

              <span v-if="review.toilet_id" class="text-xs text-gray-400">
                @ {{ toiletTitleMap[review.toilet_id] }}</span
              >
            </div>

            <UButton
              icon="i-heroicons-heart"
              variant="ghost"
              color="error"
              :disabled="true"
            >
              <span class="text-sm">{{ reactionMap[review.id] || 0 }}</span>
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
