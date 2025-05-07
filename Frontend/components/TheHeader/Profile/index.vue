<script setup lang="ts">
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/user";
import ProfileReview from "./ProfileReview.vue";

const showPopover = ref(false);
const activeTab = ref(0);
const favorites = ref([]);
const reviews = ref([]);
const isLoading = ref(true);
const userStore = useUserStore();

onMounted(async () => {
  const userId = userStore?.id;

  try {
    const [favRes, revRes] = await Promise.all([
      fetch(`${BASE_URL}/favorites/list/${userId}`),
      fetch(`${BASE_URL}/reviews/user/${userId}`),
    ]);
    console.log(userId);
    favorites.value = await favRes.json();
    reviews.value = await revRes.json();
  } catch (err) {
    console.error("載入個人資料失敗", err);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <UPopover
    v-model:open="showPopover"
    :popper="{ placement: 'bottom-end' }"
    :ui="{
      content:
        'w-[40vw] max-w-[480px] p-4 rounded-lg shadow-lg bg-white dark:bg-gray-900',
    }"
  >
    <!-- 觸發按鈕 -->
    <UButton
      icon="i-heroicons-user-circle"
      color="info"
      variant="soft"
      size="md"
      label="個人資料"
    />

    <!-- Popover 內容 -->
    <template #content>
      <UTabs
        v-model="activeTab"
        :items="[{ label: '最愛' }, { label: '評論' }, { label: '統計' }]"
      >
        <template #content="{ item }">
          <!-- 載入中 -->
          <div v-if="isLoading" class="text-sm text-gray-500 px-2 py-4">
            載入中...
          </div>

          <!-- 我的最愛 -->
          <div v-else-if="item.label === '最愛'" class="space-y-2 px-2 py-2">
            <h3 class="text-sm font-semibold">❤️ 我的最愛</h3>
          </div>

          <!-- 我的評論 -->
          <div v-else-if="item.label === '評論'" class="space-y-2 px-2 py-2">
            <ProfileReview :reviews="reviews" />
          </div>
        </template>
      </UTabs>
    </template>
  </UPopover>
</template>
