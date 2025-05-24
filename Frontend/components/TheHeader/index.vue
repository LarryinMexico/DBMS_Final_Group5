<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useLocationStore } from "@/stores/location";

import ColorModeButton from "./ColorModeButton.vue";
import AddToiletButton from "./AddToiletButton.vue";
import Profile         from "./Profile/index.vue";

const userStore     = useUserStore();
const locationStore = useLocationStore();
const showProfile   = ref(false);
const hasError      = ref(false);

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
      await locationStore.locateAndRequestPan(); // 再飛一次
    } else {
      await locationStore.locateAndRequestPan();
      locationStore.toggleWatch(); // 啟動追蹤
    }
    if (locationStore.errorMsg) {
      hasError.value = true;
    } else {
      hasError.value = false;
    }
  } catch (err) {
    if (locationStore.errorMsg) {
      hasError.value = true;
    }
  }
}
</script>

<template>
  <header class="h-16 border-b px-4 flex items-center justify-end">
    <!-- 顏色切換 -->
    <ColorModeButton />

    <!-- 功能列 -->
    <div class="flex items-end gap-2">
      <!-- 我的位置 / 導航中 -->
      <UButton
        :icon="locationStore.watching ? 'i-lucide-navigation' : 'i-lucide-map-pinned'"
        size="md"
        variant="soft"
        :color="locColor"
        @click="handleLocClick"
      >
        <span class="hidden sm:inline ml-1">{{ locLabel }}</span>
      </UButton>

      <!-- 個人資料 -->
      <UButton
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

      <!-- 登入 / 登出（略，保持原樣） -->
      <SignedOut>
        <SignInButton
          mode="modal"
          afterSignInUrl="/"
          :appearance="{
            elements: { button: 'bg-green-500 hover:bg-green-600 text-white rounded px-3 py-2' },
          }"
        >
          <UButton icon="i-lucide-user" variant="soft" color="secondary">
            <span class="hidden sm:inline ml-1">登入</span>
          </UButton>
        </SignInButton>
      </SignedOut>
      <SignedIn><UserButton /></SignedIn>
    </div>
  </header>
</template>
