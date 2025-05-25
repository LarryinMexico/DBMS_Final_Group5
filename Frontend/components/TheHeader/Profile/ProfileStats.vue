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
  const res = await fetch(`${BASE_URL}/reviews/user/${props.userId}`);
  const reviews = await res.json();

  const countsByRating: Record<number, number> = {};
  const countsByBuilding: Record<string, number> = {};
  const timestamps: string[] = [];

const toiletMap = new Map<number, any>();
const buildingMap = new Map<number, any>();

for (const r of reviews) {
  // 🕒 加入時間
  timestamps.push(new Date(r.createAt).toLocaleString());

  // ⭐ 加入評分統計
  countsByRating[r.rating] = (countsByRating[r.rating] ?? 0) + 1;

  try {
    // 🚽 取得 toilet（有快取）
    let toilet = toiletMap.get(r.toilet_id);
    if (!toilet) {
      const res = await fetch(`${BASE_URL}/toilets/${r.toilet_id}`);
      if (!res.ok) throw new Error(`toilet ${r.toilet_id} fetch failed`);
      toilet = await res.json();
      toiletMap.set(r.toilet_id, toilet);
    }

    // 🏢 取得 building（有快取）
    const buildingId = toilet.building_id;
    let building = buildingMap.get(buildingId);
    if (!building) {
      const res = await fetch(`${BASE_URL}/buildings/${buildingId}`);
      if (!res.ok) throw new Error(`building ${buildingId} fetch failed`);
      building = await res.json();
      buildingMap.set(buildingId, building);
    }

    const name = building.name || "未知";
    countsByBuilding[name] = (countsByBuilding[name] ?? 0) + 1;
  } catch (err) {
    console.error("❌ 資料取得失敗：", err);
    // 若失敗仍保底加入未知分類
    countsByBuilding["未知"] = (countsByBuilding["未知"] ?? 0) + 1;
  }
}

  // 累積評論數資料
  const sortedTimestamps = timestamps
    .map((t) => new Date(t))
    .sort((a, b) => a.getTime() - b.getTime());

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

  loading.value = false;
});
</script>

<template>
  <div v-if="loading">📊 資料讀取中...</div>
  <div
    class="flex flex-col lg:flex-row flex-wrap gap-6 justify-center items-start"
  >
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
