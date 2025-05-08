<script setup lang="ts">
import { BASE_URL } from "@/constants";
import ProfileReview from "./ProfileReview.vue";
import ProfileFavorites from "./ProfileFavorites.vue";

const props = defineProps<{ userId: string }>();

const showPopover = ref(false);
const activeTab = ref(0);
const reviews = ref([]);
const isLoading = ref(true);

watch(showPopover, async (open) => {
  if (!open || !props.userId) return;

  isLoading.value = true;
  try {
    const res = await fetch(`${BASE_URL}/reviews/user/${props.userId}`);
    if (!res.ok) throw new Error("取得評論失敗");
    reviews.value = await res.json();
  } catch (err) {
    console.error("❌ 載入 review 失敗", err);
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
          <div v-if="isLoading" class="text-sm text-gray-500 px-2 py-4">
            載入中...
          </div>

          <div v-else-if="item.label === '最愛'" class="space-y-2 px-2 py-2">
            <ProfileFavorites :userId="props.userId" />
          </div>

          <div v-else-if="item.label === '評論'" class="space-y-2 px-2 py-2">
            <ProfileReview :reviews="reviews" />
          </div>
        </template>
      </UTabs>
    </template>
  </UPopover>
</template>
