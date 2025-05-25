<script setup lang="ts">
import { defineAsyncComponent, onMounted, ref } from "vue";
import { BASE_URL } from "@/constants";

const ApexChart = defineAsyncComponent(() =>
  import("vue3-apexcharts").then((mod) => mod.default),
);

const props = defineProps<{ userId: string }>();

const loading = ref(true);
const timeline = ref<{ timestamp: string; count: number }[]>([]);
const ratingStats = ref<{ rating: number; count: number }[]>([]);
const buildingStats = ref<{ building: string; count: number }[]>([]);

onMounted(async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/user/${props.userId}/full`);
    const reviews = await res.json();

    const countsByRating: Record<number, number> = {};
    const countsByBuilding: Record<string, number> = {};
    const timestamps: Date[] = [];

    for (const r of reviews) {
      // 🕒 時間統計
      timestamps.push(new Date(r.updateAt));

      // ⭐ 評分統計
      countsByRating[r.rating] = (countsByRating[r.rating] ?? 0) + 1;

      // 🏢 大樓統計
      const name = r.toilet.title || "未知";
      countsByBuilding[name] = (countsByBuilding[name] ?? 0) + 1;
    }

    // 累積評論數資料
    const sortedTimestamps = timestamps.sort((a, b) => a.getTime() - b.getTime());

    timeline.value = sortedTimestamps.map((d, i) => ({
      timestamp: d.toLocaleString(),
      count: i + 1,
    }));

    ratingStats.value = Object.entries(countsByRating)
      .sort((a, b) => +a[0] - +b[0])
      .map(([rating, count]) => ({ rating: +rating, count }));

    buildingStats.value = Object.entries(countsByBuilding).map(
      ([building, count]) => ({
        building,
        count,
      }),
    );
  } catch (err) {
    console.error("❌ enriched review 統計失敗", err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading">📊 資料讀取中...</div>
  <div class="flex flex-col lg:flex-row flex-wrap gap-6 justify-center items-start">
    <!-- 評分分佈 -->
    <div class="flex-1 min-w-0 basis-[400px]">
      <ApexChart
        type="bar"
        height="300"
        width="100%"
        :options="{
          chart: { id: 'rating-distribution' },
          title: { text: '評分分佈' },
          xaxis: {
            categories: ratingStats.map((d) => d.rating.toString()),
            title: { text: '星星數' },
          },
        }"
        :series="[
          {
            name: '評論數',
            data: ratingStats.map((d) => d.count),
          },
        ]"
      />
    </div>

    <!-- 大樓分佈 -->
    <div class="flex-1 min-w-0 basis-[400px]">
      <ApexChart
        type="donut"
        height="300"
        width="100%"
        :options="{
          chart: { id: 'building-distribution' },
          title: { text: '評論大樓分佈' },
          labels: buildingStats.map((d) => d.building),
        }"
        :series="buildingStats.map((d) => d.count)"
      />
    </div>
  </div>
</template>
