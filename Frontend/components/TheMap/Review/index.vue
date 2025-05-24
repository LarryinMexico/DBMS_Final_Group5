<script setup lang="ts">
import ReviewForm from "@/components/TheMap/Review/ReviewForm.vue";
import ReviewList from "@/components/TheMap/Review/ReviewList.vue";
import { BASE_URL } from "@/constants/index.js";

const props = defineProps<{
  toilet: { id: number; floor: string | number; type: string; title?: string };
}>();

const reloadReviews = ref(0); // 可以透過切換這個觸發重新 fetch

const triggerReload = () => {
  reloadReviews.value++;
};

const reports = ref<Array<{ id: number; description: string; status: string }>>(
  [],
);
const isLoadingReports = ref(true);

const fetchReports = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reports/toilet/${props.toilet.id}`);
    if (!res.ok) throw new Error("無法取得報修資料");
    const data = await res.json();
    reports.value = data.filter((r: any) => r.status === "pending"); // 只取待處理的
  } catch (err) {
    console.error("取得報修資料失敗", err);
  } finally {
    isLoadingReports.value = false;
  }
};

onMounted(() => {
  fetchReports();
});
</script>

<template>
  <div class="space-y-4">
    <UCard v-if="!isLoadingReports && reports.length > 0">
      <template #header> 🚧 正在處理問題 </template>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li v-for="r in reports" :key="r.id" class="pl-2 list-disc">
          {{ r.description }}
        </li>
      </ul>
    </UCard>

    <ReviewForm :toilet-id="props.toilet.id" @submitted="triggerReload" />
    <ReviewList :toilet-id="props.toilet.id" :reload="reloadReviews" />
  </div>
</template>
