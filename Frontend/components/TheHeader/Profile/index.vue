<!-- UserProfilePanel.vue -->
<script setup lang="ts">
import { BASE_URL } from "@/constants";
import ProfileReview from "./ProfileReview.vue";
import ProfileFavorites from "./ProfileFavorites.vue";

const props = defineProps<{ userId: string }>();

const reviews = ref([]);
const isLoading = ref(true);
const activeTab = ref(0);

onMounted(async () => {
  if (!props.userId) return;
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
  <div class="space-y-4">
    <UTabs
      v-model="activeTab"
      :items="[{ label: '最愛' }, { label: '評論' }, { label: '統計' }]"
    >
      <template #content="{ item }">
        <div v-if="isLoading" class="text-sm text-gray-500 py-4">
          載入中...
        </div>
        <div v-else-if="item.label === '最愛'" class="space-y-2">
          <ProfileFavorites :userId="props.userId" />
        </div>
        <div v-else-if="item.label === '評論'" class="space-y-2">
          <ProfileReview :reviews="reviews" />
        </div>
        <div v-else class="text-sm text-gray-400">🚧 尚未實作</div>
      </template>
    </UTabs>
  </div>
</template>
