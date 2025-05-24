<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { z } from "zod";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import ToiletMapSelector from "@/components/TheHeader/ToiletMapSelector.vue";
import { reverseGeocode } from "@/utils/reverseGeocode.js";
import { useToiletAPI } from "@/utils/useToiletAPI.js";
import { BASE_URL } from "~/constants";
import { useAuth } from "@clerk/vue";
import { useBuildingStore } from "~/stores/building";

const typeLabelMap = {
  male: "男廁",
  female: "女廁",
  unisex: "性別友善廁所",
  accessible: "無障礙廁所",
};

const buildingStore = useBuildingStore();
const { postToilet } = useToiletAPI();
const { getToken } = useAuth();

const isOpen = ref(false);
const isSubmitting = ref(false);
const location = ref({ lng: 121.5773869, lat: 24.9878484 });
const locationSource = ref("building");
const address = reverseGeocode(location.value.lng, location.value.lat);

const buildingOptions = ref([]);
const buildingMap = ref({});

watch(location, async (newLocation) => {
  if (locationSource.value === "custom") {
    address.value = await reverseGeocode(newLocation);
    buildingName.value = address.value;
  }
});

watch(
  isSubmitting,
  async (val) => {
    if (!val) {
      const res = await fetch(`${BASE_URL}/buildings/`);
      const buildings = await res.json();

      buildingOptions.value = buildings.map((b) => ({
        label: b.name,
        value: b.id,
      }));

      buildingMap.value = Object.fromEntries(buildings.map((b) => [b.id, b]));
    }
  },
  { immediate: true },
);

const typeOptions = [
  { label: "男廁", value: "male" },
  { label: "女廁", value: "female" },
  { label: "性別友善廁所", value: "unisex" },
  { label: "無障礙廁所", value: "accessible" },
];

const toiletSchema = toTypedSchema(
  z.object({
    building: z.any().optional(),
    buildingName: z.string().optional(),
    floorMin: z.string().optional(),
    floorMax: z.string().optional(),
    floor: z.string({ required_error: "請選擇樓層" }),
    type: z.string({ required_error: "請選擇廁所類型" }),
  }),
);

const { errors, defineField, values } = useForm({
  validationSchema: toiletSchema,
});

const [building, buildingAttrs] = defineField("building");
const [buildingName, buildingNameAttrs] = defineField("buildingName");
const [floorMax, floorMaxAttrs] = defineField("floorMax");
const [floor, floorAttrs] = defineField("floor");
const [type, typeAttrs] = defineField("type");

const floorOptions = computed(() => {
  if (locationSource.value === "building") {
    const id = values.building?.value;
    const max = buildingMap.value[id]?.max_floor ?? 0;
    return Array.from({ length: max }, (_, i) => ({
      label: `${i + 1} 樓`,
      value: `${i + 1}`,
    }));
  }

  const min = Number(values.floorMin ?? 1);
  const max = Number(values.floorMax);
  if (isNaN(min) || isNaN(max) || min > max) return [];

  return Array.from({ length: max - min + 1 }, (_, i) => {
    const floorNum = min + i;
    const label = floorNum < 0 ? `B${Math.abs(floorNum)}` : `${floorNum} 樓`;
    return { label, value: `${floorNum}` };
  });
});

const isSubmitDisabled = computed(() => {
  return !values.floor || !values.type || isSubmitting.value;
});

let hasSubmitted = false;

async function onSubmit(values) {
  if (hasSubmitted) return;
  hasSubmitted = true;
  isSubmitting.value = true;

  try {
    const token = await getToken.value();
    if (!token) throw new Error("未登入");

    let building_id;

    if (locationSource.value === "custom") {
      const newBuildingRes = await fetch(`${BASE_URL}/buildings/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: values.buildingName,
          max_floor: Number(values.floorMax),
          lat: location.value.lat,
          lng: location.value.lng,
        }),
      });

      if (!newBuildingRes.ok) throw new Error("無法新增建築");
      const newBuilding = await newBuildingRes.json();
      building_id = newBuilding.id;
      await buildingStore.addBuilding(newBuilding);
    } else {
      building_id = Number(values.building?.value);
    }

    // 自動組合名稱
    const buildingNameResolved =
      buildingMap.value[building_id]?.name || values.buildingName;
    const floorLabel = `${values.floor} 樓`;
    const typeLabel = typeLabelMap[values.type.label] || values.type.label;
    const floorValue = Number(values.floor?.value);
    const composedTitle = `${buildingNameResolved} ${floorValue}樓 ${typeLabel}`;

    await postToilet({
      building_id,
      floor: floorValue,
      type: values.type.value,
      title: composedTitle,
    });
    useToast().add({
      title: "Success",
      description: "成功新增廁所資訊",
      color: "success",
    });

    isOpen.value = false;
  } catch (error) {
    console.error("送出失敗:", error);
    useToast().add({ title: "錯誤", description: error.message, color: "red" });
  } finally {
    isSubmitting.value = false;
    hasSubmitted = false;
  }
}
</script>

<template>
  <div>
    <USlideover v-model:open="isOpen" title="新增廁所資訊">
      <UButton
        icon="i-lucide-plus"
        color="success"
        variant="soft"
        @click="isOpen = true"
      >
        <span class="hidden sm:inline ml-1">個人資料</span>
      </UButton>
      <template #body>
        <div class="flex flex-col h-full justify-start gap-y-10">
          <UCard>
            <template #header>
              <h2 class="text-base font-bold">地點資訊</h2>
            </template>
            <template #default>
              <URadioGroup
                label="地點來源"
                :items="[
                  { label: '選擇現有建築', value: 'building' },
                  { label: '自行輸入位置', value: 'custom' },
                ]"
                v-model="locationSource"
              />

              <div
                v-if="locationSource === 'building'"
                class="flex flex-row justify-between py-5 space-x-2"
              >
                <USelectMenu
                  label="選擇建築"
                  :items="buildingOptions"
                  v-model="building"
                  v-bind="buildingAttrs"
                  :error="errors.building"
                  class="w-1/2"
                  :searchInput="false"
                />

                <USelectMenu
                  :searchInput="false"
                  label="選擇樓層"
                  :items="floorOptions"
                  v-model="floor"
                  v-bind="floorAttrs"
                  :error="errors.floor"
                  :disabled="!values.building"
                  class="w-1/2"
                />
              </div>

              <div v-else class="space-y-4 mt-4">
                <div class="flex gap-2">
                  <UFormField label="建築名稱" required class="w-full">
                    <UInput
                      class="w-full"
                      v-model="buildingName"
                      v-bind="buildingNameAttrs"
                    />
                  </UFormField>
                </div>

                <div class="flex gap-2">
                  <UFormField label="最高樓層" required class="w-full">
                    <UInput
                      type="number"
                      v-model="floorMax"
                      v-bind="floorMaxAttrs"
                      class="w-full"
                    />
                  </UFormField>
                  <UFormField label="新增樓層" required class="w-full">
                    <USelectMenu
                      label="新增樓層"
                      :items="floorOptions"
                      v-model="floor"
                      v-bind="floorAttrs"
                      :error="errors.floor"
                      :searchInput="false"
                      class="w-full"
                    />
                  </UFormField>
                </div>
                <ToiletMapSelector
                  v-model="location"
                  class="mt-2 rounded overflow-hidden h-72"
                />
              </div>
            </template>
          </UCard>

          <UCard>
            <template #header>
              <h2 class="text-base font-bold">廁所資訊</h2>
            </template>
            <template #default>
              <div class="flex flex-row justify-between py-5 space-x-2">
                <USelectMenu
                  :searchInput="false"
                  label="廁所類型"
                  :items="typeOptions"
                  v-model="type"
                  v-bind="typeAttrs"
                  :error="errors.type"
                  class="w-1/2"
                />
              </div>
            </template>
          </UCard>
        </div>
      </template>
      <template #footer>
        <UButton
          type="submit"
          color="primary"
          block
          :loading="isSubmitting"
          :disabled="isSubmitDisabled"
          @click="onSubmit(values)"
        >
          送出
        </UButton>
      </template>
    </USlideover>
  </div>
</template>
