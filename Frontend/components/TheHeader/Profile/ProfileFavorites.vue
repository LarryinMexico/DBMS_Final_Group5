<script setup lang="ts">
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/user";

const props = defineProps<{ userId: string }>();

/* ------------------------------ state ------------------------------ */
// favourites of the profile owner (used to決定要顯示哪些廁所卡片)
const ownerFavoriteIds = ref<number[]>([]);
// favourites of the logged-in user (用來決定按鈕 UI 與 toggle 行為)
const myFavoriteSet = ref<Set<number>>(new Set());

const toilets = ref<any[]>([]);
const stats = ref<Record<number, { avg_rating: number; count: number }>>({});

const isLoading = ref(true);
const toast = useToast();
const userStore = useUserStore();

const isSelf = computed(() => props.userId === String(userStore.id)); // 是否在看自己的頁面

/* ----------------------------- fetchers ---------------------------- */
const fetchOwnerFavoritesAndToilets = async () => {
  const res = await fetch(`${BASE_URL}/favorites/list/${props.userId}`);
  if (!res.ok) throw new Error("無法取得頁面擁有者的最愛");
  const favRows = await res.json();
  ownerFavoriteIds.value = favRows.map((f: any) => f.toilet_id);

  // 只抓擁有者最愛對應的廁所資料
  const toiletRes = await Promise.all(
    ownerFavoriteIds.value.map((id) => fetch(`${BASE_URL}/toilets/${id}`)),
  );
  toilets.value = await Promise.all(toiletRes.map((r) => r.json()));
};

const fetchMyFavorites = async () => {
  if (!userStore.id) return; // 遊客直接跳過
  if (isSelf.value) {
    // 觀看自己時，直接沿用 ownerFavoriteIds
    myFavoriteSet.value = new Set(ownerFavoriteIds.value);
    return;
  }
  const res = await fetch(`${BASE_URL}/favorites/list/${userStore.id}`);
  if (!res.ok) throw new Error("無法取得自己的最愛");
  const rows = await res.json();
  myFavoriteSet.value = new Set(rows.map((r: any) => r.toilet_id));
};

const fetchStats = async () => {
  const res = await fetch(`${BASE_URL}/reviews/stats`);
  const data = await res.json();
  stats.value = Object.fromEntries(
    data.map((d: any) => [
      d.toilet_id,
      { avg_rating: d.avg_rating, count: d.count },
    ]),
  );
};

/* --------------------------- interaction --------------------------- */
const toggleFavorite = async (toiletId: number) => {
  if (!userStore.id) {
    toast.add({ title: "請先登入", color: "error" });
    return;
  }

  const already = myFavoriteSet.value.has(toiletId);
  const method = already ? "DELETE" : "POST";
  const url = `${BASE_URL}/favorites/${already ? "delete" : "add"}`;

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userStore.id, toilet_id: toiletId }),
  });

  if (!res.ok) {
    toast.add({ title: "操作失敗", description: "請稍後再試", color: "error" });
    return;
  }

  // 更新自己的收藏集合
  already
    ? myFavoriteSet.value.delete(toiletId)
    : myFavoriteSet.value.add(toiletId);

  toast.add({
    title: already ? "已移除最愛" : "成功加入最愛",
    color: already ? "error" : "success",
  });

  // 若正在看自己的頁面，同步 ownerFavoriteIds 才能立即反映列表
  if (isSelf.value) {
    ownerFavoriteIds.value = Array.from(myFavoriteSet.value);
  }
};

/* ------------------------------ init ------------------------------- */
onMounted(async () => {
  try {
    await Promise.all([fetchOwnerFavoritesAndToilets(), fetchStats()]);
    await fetchMyFavorites();
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="space-y-3">
    <UCard
      v-for="toilet in toilets"
      :key="toilet.id"
      class="border border-gray-200 dark:border-gray-700 p-4"
    >
      <!-- 標題 -->
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-base font-bold">
          {{ toilet.title || "無名稱" }}
          <span class="text-sm text-gray-400 ml-1"
            >📍{{ toilet.floor }} 樓</span
          >
        </h3>
      </div>

      <!-- 評分與最愛 -->
      <div class="flex items-center space-x-4 text-sm text-red-500">
        <!-- 星星 -->
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
        <!-- 評論數 -->
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-chat-bubble-left-right" />
          <span>{{ stats[toilet.id]?.count || 0 }} 則</span>
        </div>

        <!-- 我的最愛按鈕（總是根據自己是否已收藏來顯示） -->
        <UButton
          v-if="!isLoading"
          :label="myFavoriteSet.has(toilet.id) ? '已加入' : '加入最愛'"
          :color="myFavoriteSet.has(toilet.id) ? 'success' : 'error'"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
          @click.stop="toggleFavorite(toilet.id)"
        />

        <!-- loading state -->
        <UButton v-else loading variant="soft" color="neutral" size="xs" />
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 尚未加入任何最愛
    </p>
  </div>
</template>
