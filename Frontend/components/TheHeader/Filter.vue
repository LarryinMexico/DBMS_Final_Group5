<script setup lang="ts">
import { BASE_URL } from "~/constants";
import type { Amenity } from "../TheMap/ToiletCardList.vue";

const emit = defineEmits<{
  (e: "update:filters", value: FilterOptions): void;
}>();

export interface FilterOptions {
  floorMax?: number;
  reviewCountMin?: number;
  averageRatingMin?: number;
  accessible?: boolean;
  gender?: "male" | "female" | "unisex";
  amenities?: number[];
}

const filters = ref<FilterOptions>({});

// 基本篩選條件
const floorMax = ref<number | null>(null);
const accessible = ref(false);
const gender = ref<"male" | "female" | "unisex" | null>(null);

// 評論與評分條件
const reviewCountMin = ref<number | null>(null);
const averageRatingMin = ref(1);

// 備品條件
const selectedAmenities = ref<number[]>([]);
const allAmenities = ref<Amenity[]>([]);

const fetchAllAmenities = async () => {
  try {
    const res = await fetch(`${BASE_URL}/amenities/`);
    if (!res.ok) throw new Error("載入備品失敗");
    allAmenities.value = await res.json();
  } catch (err) {
    console.error("❌ 載入備品失敗", err);
    allAmenities.value = [];
  }
};

onMounted(fetchAllAmenities);

const isLoading = ref(false);

const update = async () => {
  isLoading.value = true;

  // 假裝 loading 1 秒
  await new Promise((resolve) => setTimeout(resolve, 1000));

  filters.value = {
    floorMax: floorMax.value ?? undefined,
    accessible: accessible.value || undefined,
    gender: gender.value ?? undefined,
    reviewCountMin: reviewCountMin.value ?? undefined,
    averageRatingMin: averageRatingMin.value ?? undefined,
    amenities:
      selectedAmenities.value.length > 0 ? selectedAmenities.value : undefined,
  };

  emit("update:filters", filters.value);

  isLoading.value = false;
};
</script>

<template>
  <div class="space-y-5">
    <!-- 樓層上限 -->
    <div>
      <label class="font-semibold">樓層小於</label>
      <UInput
        v-model.number="floorMax"
        type="number"
        :min="0"
        placeholder="例如：10"
        class="w-full"
      />
    </div>

    <!-- 評論數量下限 -->
    <div>
      <label class="font-semibold">最少評論數</label>
      <UInput
        v-model.number="reviewCountMin"
        type="number"
        :min="0"
        placeholder="例如：3"
        class="w-full"
      />
    </div>

    <div>
      <label class="font-semibold flex justify-between items-center">
        最低平均評分
        <span class="text-sm text-gray-500">{{
          averageRatingMin.toFixed(1)
        }}</span>
      </label>
      <USlider
        v-model="averageRatingMin"
        :min="1"
        :max="5"
        :step="0.5"
        class="w-full"
      />
    </div>

    <div>
      <label class="font-semibold">備品（可複選）</label>
      <div class="flex flex-wrap gap-2">
        <UButton
          v-for="a in allAmenities"
          :key="a.id"
          :label="a.name"
          size="sm"
          variant="soft"
          :color="selectedAmenities.includes(a.id) ? 'primary' : 'neutral'"
          @click="
            selectedAmenities.includes(a.id)
              ? selectedAmenities.splice(selectedAmenities.indexOf(a.id), 1)
              : selectedAmenities.push(a.id)
          "
        />
      </div>
    </div>

    <div class="pt-2 flex justify-end">
      <UButton
        color="primary"
        icon="i-heroicons-rocket-launch"
        @click="update"
        :loading="isLoading"
        :disabled="isLoading"
      >
        套用條件
      </UButton>
    </div>
  </div>
</template>

<style scoped>
label {
  display: block;
  margin-bottom: 0.25rem;
}
</style>
