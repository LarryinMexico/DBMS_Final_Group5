<script setup lang="ts">
import { BASE_URL } from "@/constants";

const props = defineProps<{ userId: string }>();

const favoritesSet = ref<Set<number>>(new Set());
const toilets = ref<any[]>([]);
const stats = ref<Record<number, { avg_rating: number; count: number }>>({});
const isLoading = ref(true);

const toast = useToast();
const userStore = useUserStore();

const fetchFavoritesAndToilets = async () => {
  try {
    const favRes = await fetch(`${BASE_URL}/favorites/list/${props.userId}`);
    if (!favRes.ok) throw new Error("無法取得最愛");

    const favData = await favRes.json();
    const toiletIds = favData.map((f: any) => f.toilet_id);
    favoritesSet.value = new Set(toiletIds);

    const toiletResList = await Promise.all(
      toiletIds.map((id: number) => fetch(`${BASE_URL}/toilets/${id}`)),
    );

    const toiletData = await Promise.all(
      toiletResList.map((res) => res.json()),
    );
    toilets.value = toiletData;
  } catch (err) {
    console.error("❌ 載入最愛失敗", err);
  }
};

const fetchStats = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/stats`);
    const data = await res.json();
    stats.value = Object.fromEntries(
      data.map((item: any) => [
        item.toilet_id,
        { avg_rating: item.avg_rating, count: item.count },
      ]),
    );
  } catch (err) {
    console.error("❌ 載入 stats 失敗", err);
  }
};

const toggleFavorite = async (toiletId: number) => {
  const isFavorited = favoritesSet.value.has(toiletId);
  const method = isFavorited ? "DELETE" : "POST";
  const endpoint = `${BASE_URL}/favorites/${isFavorited ? "delete" : "add"}`;
  const payload = JSON.stringify({
    user_id: userStore.id,
    toilet_id: toiletId,
  });

  const res = await fetch(endpoint, {
    method,
    headers: { "Content-Type": "application/json" },
    body: payload,
  });

  if (res.ok) {
    if (isFavorited) {
      favoritesSet.value.delete(toiletId);
      toast.add({ title: "已移除最愛", color: "error" });
    } else {
      favoritesSet.value.add(toiletId);
      toast.add({ title: "成功加入最愛", color: "success" });
    }
  } else {
    toast.add({ title: "操作失敗", description: "請稍後再試", color: "error" });
  }
};

onMounted(async () => {
  await Promise.all([fetchFavoritesAndToilets(), fetchStats()]);
  console.log("最愛", favoritesSet.value);
  isLoading.value = false;
});
</script>

<template>
  <div class="space-y-3">
    <UCard
      v-for="toilet in toilets"
      :key="toilet.id"
      class="border border-gray-200 dark:border-gray-700 p-4"
    >
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-base font-bold">
          {{ toilet.title || "無名稱" }}
          <span class="text-sm text-gray-400 ml-1"
            >📍{{ toilet.floor }} 樓</span
          >
        </h3>
      </div>

      <div class="flex items-center space-x-4 text-sm text-red-500">
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-star-solid" />
          <span>
            {{
              stats[toilet.id]?.avg_rating
                ? stats[toilet.id].avg_rating.toFixed(1)
                : "尚無評分"
            }}
          </span>
        </div>

        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-chat-bubble-left-right" />
          <span>{{ stats[toilet.id]?.count || 0 }} 則</span>
        </div>

        <UButton
          v-if="!isLoading"
          :label="favoritesSet.has(toilet.id) ? '已加入' : '我的最愛'"
          :color="favoritesSet.has(toilet.id) ? 'success' : 'error'"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
          @click.stop="toggleFavorite(toilet.id)"
        />

        <UButton v-else loading variant="soft" color="neutral" size="xs" />
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 尚未加入任何最愛
    </p>
  </div>
</template>
