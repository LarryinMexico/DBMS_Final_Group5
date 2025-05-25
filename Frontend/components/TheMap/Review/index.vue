<script setup lang="ts">
import ReviewForm from "@/components/TheMap/Review/ReviewForm.vue";
import ReviewList from "@/components/TheMap/Review/ReviewList.vue";
import { BASE_URL } from "@/constants/index.js";

import type { Amenity } from "../ToiletCardList.vue";

const toast = useToast();
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
  fetchAmenitiesForToilet(props.toilet.id);
});

const isLoadingAmenities = ref(true);
const amenitiesForToilet = ref<Amenity[]>([]);

const fetchAmenitiesForToilet = async (toiletId: number) => {
  isLoadingAmenities.value = true;
  try {
    const res = await fetch(
      `${BASE_URL}/amenities/toilet/${toiletId}/amenities`,
    );
    if (!res.ok) throw new Error("載入備品失敗");
    const data = await res.json();
    amenitiesForToilet.value = data;
  } catch (err) {
    toast.add({ title: "載入備品失敗", color: "error" });
    amenitiesForToilet.value = [];
  } finally {
    isLoadingAmenities.value = false;
  }
};
</script>

<template>
  <div class="space-y-4">
    <UCard v-if="!isLoadingReports">
      <div class="space-y-3">
        <div class="mb-3">
          <h3
            class="flex items-center gap-2 text-base font-medium text-gray-800 dark:text-gray-200 mb-2"
          >
            <UIcon
              name="i-heroicons-exclamation-triangle"
              class="text-red-500 mt-0.5"
              size="20"
            />
            問題回報
          </h3>
          <div class="space-y-2">
          <div
              v-if="reports.length === 0"
              class="p-2 bg-gray-50 dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700"
            >
            <p class="text-sm text-gray-600 dark:text-gray-300">
              此廁所目前沒有待處理的報修 🥳
            </p>
          </div>
          <div v-if="isLoadingReports" class="text-gray-500">載入中...</div>
          <div v-else>
            <div
              v-for="r in reports"
              :key="r.id"
              class="p-2 bg-red-50 dark:bg-red-900/20 rounded border border-red-100 dark:border-red-800/30"
            >
              <p class="text-sm text-gray-700 dark:text-gray-300">
                {{ r.description }}
              </p>
            </div>
            </div>
          </div>
        </div>

        <div
          v-if="amenitiesForToilet.length > 0"
          class="pt-2 border-t border-gray-200 dark:border-gray-700 space-y-1"
        >
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            已設定備品
          </div>
          <div class="flex flex-wrap gap-2">
            <UBadge
              v-for="item in amenitiesForToilet"
              :key="item.id"
              color="primary"
              variant="soft"
            >
              {{ item.name }}
            </UBadge>
          </div>
        </div>
      </div>
    </UCard>

    <ReviewForm :toilet-id="props.toilet.id" @submitted="triggerReload" />
    <ReviewList :toilet-id="props.toilet.id" :reload="reloadReviews" />
  </div>
</template>
