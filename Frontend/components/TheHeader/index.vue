<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useLocationStore } from "@/stores/location";

import ColorModeButton from "./ColorModeButton.vue";
import AddToiletButton from "./AddToiletButton.vue";
import Profile from "./Profile/index.vue";
import Filter from "./Filter.vue";
import type { FilterOptions } from "./Filter.vue";
import ReportListModal from "./ReportListModal.vue";
import ToiletCard from "./ToiletCard.vue";
import { BASE_URL } from "~/constants";
import { useRouteStore } from "@/stores/useRouteStore";
import { useOnboarding } from "@/utils/useOnboarding";

useSocket();

const routeStore = useRouteStore();

const userStore = useUserStore();
const locationStore = useLocationStore();
const showProfile = ref(false);
const hasError = ref(false);
const showFilter = ref(false);
const showReportModal = ref(false);

/* 按鈕動態屬性 */
const locLabel = computed(() =>
  hasError.value ? "錯誤" : locationStore.watching ? "導航中" : "我的位置",
);
const locColor = computed(() =>
  hasError.value ? "error" : locationStore.watching ? "success" : "info",
);
/* 點擊：未追蹤 → 一次定位 + 開追蹤；追蹤中 → 停止追蹤 */
async function handleLocClick() {
  try {
    if (locationStore.watching) {
      locationStore.toggleWatch(); // 停止追蹤
      await locationStore.locateAndRequestPan(); // 再定位一次
    } else {
      await locationStore.locateAndRequestPan(); // 開始定位
      locationStore.toggleWatch(); // 啟動追蹤
    }

    hasError.value = !!locationStore.errorMsg;
  } catch (err) {
    hasError.value = !!locationStore.errorMsg;
  }
}

const loading = ref(false);
const results = ref<any[]>([]);
const hasSearched = ref(false); // ✅ 控制是否顯示結果

const onFilterUpdate = async (f: FilterOptions) => {
  loading.value = true;
  hasSearched.value = true;
  results.value = [];
  try {
    const res = await fetch(`${BASE_URL}/search/toilets/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        max_floor: f.floorMax,
        min_review_count: f.reviewCountMin,
        min_average_rating: f.averageRatingMin,
        amenity_ids: f.amenities?.map(Number) || [],
      }),
    });

    if (!res.ok) throw new Error("搜尋失敗");
    const data = await res.json();
    results.value = data;
  } catch (err) {
    console.error("❌ 搜尋失敗", err);
    results.value = [];
  } finally {
    loading.value = false;
  }
};

watch(showFilter, (val) => {
  if (!val) {
    hasSearched.value = false;
    results.value = [];
  }
});

const { isSignedIn } = useUser();

const showModal = computed(() => {
  return !isSignedIn.value;
});

onMounted(async () => {
  if (typeof window === "undefined") return; // 確保 client only

  await nextTick(); // 等待 DOM 渲染

  setTimeout(() => {
    const shown = localStorage.getItem("headerTourDone");
    if (!shown && isSignedIn.value) {
      const { startTour } = useOnboarding();
      startTour();
      localStorage.setItem("headerTourDone", "true");
    }
  }, 500); // 延遲 500ms 避免與 SSR hydration 衝突
});
</script>

<template>
  <header class="h-16 border-b px-4 flex items-center justify-end">
    <!-- 顏色切換 -->
    <ColorModeButton />

    <!-- 功能列 -->
    <div class="flex items-end gap-2">
      <UButton
        class="filter-btn"
        icon="i-lucide-filter"
        size="md"
        variant="soft"
        color="info"
        @click="showFilter = true"
      >
        <span class="hidden sm:inline ml-1">篩選</span>
      </UButton>

      <UButton
        v-if="routeStore.routeGeoJSON"
        icon="i-lucide-x-circle"
        size="md"
        color="warning"
        variant="soft"
        @click="routeStore.clearRoute"
      >
        <span class="hidden sm:inline ml-1">清除路徑</span>
      </UButton>

      <!-- 我的位置 / 導航中 -->
      <UButton
        class="locate-btn"
        :icon="
          hasError
            ? 'i-lucide-alert-triangle'
            : locationStore.watching
              ? 'i-lucide-navigation'
              : 'i-lucide-map-pin'
        "
        size="md"
        variant="soft"
        :color="locColor"
        @click="handleLocClick"
      >
        <span class="hidden sm:inline ml-1">{{ locLabel }}</span>
      </UButton>

      <!-- 個人資料 -->
      <UButton
        class="profile-btn"
        icon="i-heroicons-user-circle"
        size="md"
        variant="soft"
        color="info"
        @click="showProfile = true"
      >
        <span class="hidden sm:inline ml-1">個人資料</span>
      </UButton>

      <UModal v-model:open="showProfile">
        <template #content>
          <Profile
            :userId="userStore.id?.toString() || ''"
            @close="showProfile = false"
          />
        </template>
      </UModal>

      <!-- 新增廁所 -->
      <AddToiletButton />

      <!-- 報修列表（只顯示給管理員） -->
      <UTooltip v-if="!userStore.isAdmin" text="僅限管理員">
        <div>
          <UButton
            icon="i-lucide-wrench"
            size="md"
            variant="soft"
            color="warning"
            :disabled="true"
          >
            <span class="hidden sm:inline ml-1">報修列表</span>
          </UButton>
        </div>
      </UTooltip>
      <UButton
        v-else
        icon="i-lucide-wrench"
        size="md"
        variant="soft"
        color="warning"
        @click="showReportModal = true"
      >
        <span class="hidden sm:inline ml-1">報修列表</span>
      </UButton>

      <!-- 登入 / 登出（略，保持原樣） -->
      <SignedOut>
        <SignInButton
          mode="modal"
          afterSignInUrl="/"
          :appearance="{
            elements: {
              button:
                'bg-green-500 hover:bg-green-600 text-white rounded px-3 py-2',
            },
          }"
        >
          <UButton icon="i-lucide-user" variant="soft" color="secondary">
            <span class="hidden sm:inline ml-1">登入</span>
          </UButton>
        </SignInButton>
      </SignedOut>
      <SignedIn><UserButton /></SignedIn>
      <UModal v-model:open="showModal" :dismissible="false">
        <template #header>
          <div class="text-lg font-bold">請先登入</div>
        </template>

        <template #body>
          <SignIn
            :appearance="{
              elements: {
                button:
                  'bg-green-500 hover:bg-green-600 text-white rounded px-3 py-2',
              },
            }"
          />
        </template>
      </UModal>
    </div>
  </header>
  <UModal v-model:open="showFilter">
    <template #header>
      <h2 class="text-xl font-bold">🔍 篩選條件</h2>
      <UButton
        icon="i-lucide-x"
        variant="link"
        class="absolute right-4 top-4"
        @click="showFilter = false"
      />
    </template>
    <template #body>
      <div class="p-4 space-y-6">
        <template v-if="!hasSearched">
          <Filter @update:filters="onFilterUpdate" />
        </template>
        <template v-if="hasSearched">
          <div v-if="loading">
            <USkeleton class="h-24 rounded-lg" v-for="i in 3" :key="i" />
          </div>

          <div v-else-if="results.length === 0">
            <p class="text-sm text-gray-400 text-center mt-4">
              😢 找不到符合的廁所
            </p>
          </div>

          <div v-else class="space-y-4">
            <ToiletCard
              v-for="toilet in results"
              :key="toilet.id"
              :id="toilet.id"
              @close="showFilter = false"
            />
          </div>
        </template>
      </div>
    </template>
  </UModal>

  <ReportListModal :open="showReportModal" @close="showReportModal = false" />
</template>
