<script setup lang="ts">
import { BASE_URL } from "~/constants";
import { useLocationStore } from "@/stores/location";
import { useUserStore } from "@/stores/user";
import { useToast } from "#imports";
import { useRouteStore } from "@/stores/useRouteStore";

interface Toilet {
  id: number;
  building_id: number;
  title: string;
  floor: string;
}

interface Building {
  id: number;
  name: string;
  lat: number;
  lng: number;
}
const VITE_MAPBOX_TOKEN =
  "pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng";

const props = defineProps<{ id: number }>();

const toilet = ref<Toilet | null>(null);
const building = ref<Building | null>(null);
const walkingDistance = ref<number | null>(null);

const stats = ref<Record<number, { avg_rating: number; count: number }>>({});
const favorites = ref<Set<number>>(new Set());
const isLoading = ref(true);

const locationStore = useLocationStore();
const userStore = useUserStore();
const routeStore = useRouteStore();
const toast = useToast();

const fetchStats = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/stats`);
    if (!res.ok) throw new Error("取得評論統計失敗");
    const data = await res.json();
    stats.value = Object.fromEntries(
      data.map((item: any) => [
        item.toilet_id,
        { avg_rating: item.avg_rating, count: item.count },
      ]),
    );
  } catch (err) {
    console.error("❌ 無法取得 stats", err);
  }
};

const fetchFavorites = async () => {
  const userId = userStore?.id;
  if (!userId) return;
  const res = await fetch(`${BASE_URL}/favorites/list/${userId}`);
  const data = await res.json();
  favorites.value = new Set(data.map((item: any) => item.toilet_id));
};

const toggleFavorite = async (toiletId: number) => {
  const userId = userStore?.id;
  if (!userId) return;
  const isFavorited = favorites.value.has(toiletId);
  const method = isFavorited ? "DELETE" : "POST";
  const endpoint = `${BASE_URL}/favorites/${isFavorited ? "delete" : "add"}`;
  const payload = JSON.stringify({ user_id: userId, toilet_id: toiletId });

  const res = await fetch(endpoint, {
    method,
    headers: { "Content-Type": "application/json" },
    body: payload,
  });

  if (res.ok) {
    if (isFavorited) {
      favorites.value.delete(toiletId);
      toast.add({ title: "已移除最愛", color: "error" });
    } else {
      favorites.value.add(toiletId);
      toast.add({ title: "成功加入最愛", color: "success" });
    }
  }
};

function goToMapRoute() {
  if (!locationStore.coords || !building.value) return;

  const from = locationStore.coords;
  const to = { lat: building.value.lat, lng: building.value.lng };
  routeStore.fetchRoute(from, to); // 🔥 這邊觸發
  emit("close");
}

onMounted(async () => {
  const toiletRes = await fetch(`${BASE_URL}/toilets/${props.id}`);
  if (toiletRes.ok) toilet.value = await toiletRes.json();

  if (toilet.value?.building_id) {
    const bRes = await fetch(
      `${BASE_URL}/buildings/${toilet.value.building_id}`,
    );
    if (bRes.ok) building.value = await bRes.json();
  }

  const user = locationStore.coords;
  if (user && building.value) {
    const res = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/walking/${user.lng},${user.lat};${building.value.lng},${building.value.lat}?access_token=${VITE_MAPBOX_TOKEN}`,
    );
    const data = await res.json();
    walkingDistance.value = data.routes?.[0]?.distance
      ? Math.round(data.routes[0].distance)
      : null;
  }

  await Promise.all([fetchStats(), fetchFavorites()]);
  isLoading.value = false;
});
const emit = defineEmits<{
  (e: "close"): void;
}>();
</script>

<template>
  <UCard
    v-if="toilet && building"
    class="border border-gray-200 dark:border-gray-700 p-4"
  >
    <!-- 上排：名稱 + 導航 -->
    <div class="flex justify-between items-center mb-2">
      <h2 class="text-base font-bold">
        {{ toilet.title || "無名稱" }}
      </h2>
      <UButton
        icon="i-lucide-navigation"
        size="sm"
        color="primary"
        variant="soft"
        :disabled="!locationStore.coords || isLoading"
        @click="
          () => {
            goToMapRoute();
          }
        "
      >
        導航
      </UButton>
    </div>

    <!-- 評論統計 + 最愛 -->
    <div class="flex items-center space-x-4 text-sm text-red-500 mb-1">
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
        :label="favorites.has(toilet.id) ? '已加入' : '我的最愛'"
        :color="favorites.has(toilet.id) ? 'success' : 'error'"
        variant="soft"
        icon="i-heroicons-heart"
        size="xs"
        @click.stop="toggleFavorite(toilet.id)"
      />
      <!-- 距離顯示 -->
      <p v-if="walkingDistance !== null" class="text-xs text-gray-400">
        📍 約 {{ walkingDistance }} 公尺（步行）
      </p>
      <p v-else class="text-xs text-gray-400">開啟導航功能以查看距離</p>
    </div>
  </UCard>

  <USkeleton v-else class="h-24 rounded-lg" />
</template>
