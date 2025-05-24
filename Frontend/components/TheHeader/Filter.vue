<script setup lang="ts">
import { ref, watch } from "vue";

// 模擬傳入的 props 或 emit，後續可調整
const emit = defineEmits<{
  (e: "update:filters", value: FilterOptions): void;
}>();

export interface FilterOptions {
  floor?: number;
  accessible?: boolean;
  gender?: "male" | "female" | "unisex";
}

const filters = ref<FilterOptions>({});

const floor = ref<number | null>(null);
const accessible = ref(false);
const gender = ref<"male" | "female" | "unisex" | null>(null);

watch([floor, accessible, gender], () => {
  filters.value = {
    floor: floor.value ?? undefined,
    accessible: accessible.value || undefined,
    gender: gender.value ?? undefined,
  };
  emit("update:filters", filters.value);
});
</script>

<template>
  <div class="space-y-4">
    <div>
      <label class="font-semibold">樓層</label>
      <UInput
        v-model.number="floor"
        type="number"
        placeholder="例如：1、2、3"
        class="w-full"
      />
    </div>

    <div>
      <label class="font-semibold">無障礙廁所</label>
      <UToggle v-model="accessible" />
    </div>

    <div>
      <label class="font-semibold">性別</label>
      <URadioGroup
        v-model="gender"
        :options="[
          { label: '不指定', value: null },
          { label: '男生', value: 'male' },
          { label: '女生', value: 'female' },
          { label: '共用', value: 'unisex' },
        ]"
        class="w-full"
      />
    </div>
  </div>
</template>

<style scoped>
label {
  display: block;
  margin-bottom: 0.25rem;
}
</style>
