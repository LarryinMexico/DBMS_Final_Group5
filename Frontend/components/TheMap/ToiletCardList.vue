<script setup lang="ts">
import { useToast } from "#imports";
import { BASE_URL } from "@/constants/index.js";
import { useUserStore } from "@/stores/user";
import { useAuth } from "@clerk/vue";

const colorMode = useColorMode();

const props = defineProps<{
  toilets: Array<{
    id: number;
    floor: string | number;
    type: string;
    title?: string;
  }>;
}>();

interface Amenity {
  id: number;
  name: string;
  available: boolean; // ✅ 是否已綁定在此廁所上
}

const emit = defineEmits(["select"]);

const favorites = ref<Set<number>>(new Set());
const stats = ref<Record<number, { avg_rating: number; count: number }>>({});
const toast = useToast();
const isLoading = ref(true);
const isReporting = ref(false);
const isAdmin = computed(() => userStore?.isAdmin);

/* Amenity 相關 */
const selectedTab = ref<"report" | "amenity">("report");
const allAmenities = ref<Amenity[]>([]); // 所有備品項目
const toiletAmenities = ref<Set<number>>(new Set()); // 目前此廁所的已選 amenity_id

const fetchAmenityData = async (toiletId: number) => {
  // 所有備品種類
  const allRes = await fetch(`${BASE_URL}/amenities/`);
  const all = await allRes.json();
  allAmenities.value = all;

  // 該廁所的備品
  const assignedRes = await fetch(
    `${BASE_URL}/amenities/toilet/${toiletId}/amenities`,
  );
  const assigned = await assignedRes.json();
  toiletAmenities.value = new Set(assigned.map((a: any) => a.id));
  // ✅ 預設勾選（重點）
  selectedAmenities.value = [...toiletAmenities.value];
  console.log("已載入備品資料", {
    allAmenities: all,
    selectedAmenities: selectedAmenities.value,
  });
};

const saveAmenities = async () => {
  const toiletId = reportToilet.value?.id;
  if (!toiletId) return;

  const prevSet = new Set(toiletAmenities.value);
  const nextSet = new Set(selectedAmenities.value);

  const toAdd = [...nextSet].filter((id) => !prevSet.has(id));
  const toRemove = [...prevSet].filter((id) => !nextSet.has(id));

  await Promise.all([
    ...toAdd.map((id) =>
      fetch(`${BASE_URL}/amenities/toilet/${toiletId}/amenity/${id}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
    ),
    ...toRemove.map((id) =>
      fetch(`${BASE_URL}/amenities/toilet/${toiletId}/amenity/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
    ),
  ]);

  toiletAmenities.value = new Set(selectedAmenities.value); // 更新本地 cache
  toast.add({ title: "備品設定已儲存", color: "success" });
};

const editToilet = ref<{ id: number; title?: string } | null>(null);
const editTitle = ref("");
const isEditing = computed(() => !!editToilet.value);

const { getToken } = useAuth();
const token = await getToken.value();

const fetchFavorites = async () => {
  const userId = userStore?.id;
  if (!userId) return;

  try {
    const res = await fetch(`${BASE_URL}/favorites/list/${userId}`);
    if (!res.ok) throw new Error("取得最愛失敗");

    const data = await res.json();
    const ids = data.map((item: { toilet_id: number }) => item.toilet_id);
    favorites.value = new Set(ids);
  } catch (error) {
    console.error("❌ 無法載入最愛列表", error);
  }
};

const fetchStats = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reviews/stats`);
    if (!res.ok) throw new Error("取得評論統計失敗");

    const data = await res.json();
    stats.value = Object.fromEntries(
      data.map((item: any) => [
        item.toilet_id,
        { avg_rating: item.avg_rating, count: item.count },
      ]),
    );
  } catch (err) {
    console.error("❌ 無法取得 stats", err);
  }
};

onMounted(async () => {
  await Promise.all([fetchFavorites(), fetchStats()]);
  isLoading.value = false;
});

const userStore = useUserStore();

const toggleFavorite = async (toiletId: number) => {
  const userId = userStore?.id;
  if (!userId) return;

  const toast = useToast();
  const isFavorited = favorites.value.has(toiletId);
  const method = isFavorited ? "DELETE" : "POST";
  const endpoint = `${BASE_URL}/favorites/${isFavorited ? "delete" : "add"}`;
  const payload = JSON.stringify({ user_id: userId, toilet_id: toiletId });

  const res = await fetch(endpoint, {
    method,
    headers: { "Content-Type": "application/json" },
    body: payload,
  });

  if (res.ok) {
    if (isFavorited) {
      favorites.value.delete(toiletId);
      toast.add({ title: "已移除最愛", color: "error" });
    } else {
      favorites.value.add(toiletId);
      toast.add({ title: "成功加入最愛", color: "success" });
    }
  } else {
    toast.add({ title: "操作失敗", description: "請稍後再試", color: "error" });
  }
};

const showReportModal = ref(false);
const reportToilet = ref<{ id: number; title?: string } | null>(null);
const reportDesc = ref("");

watch(reportToilet, (newToilet) => {
  if (newToilet?.id && isAdmin.value) {
    fetchAmenityData(newToilet.id);
  }
});

const submitReport = async () => {
  const userId = userStore?.id;
  if (!userId || !reportToilet.value) return;

  isReporting.value = true;
  console.log("提交回報:", {
    user_id: userId,
    toilet_id: reportToilet.value.id,
    description: reportDesc.value,
  });

  try {
    const res = await fetch(`${BASE_URL}/reports/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        toilet_id: reportToilet.value.id,
        description: reportDesc.value,
      }),
    });

    if (!res.ok) throw new Error("回報失敗");

    toast.add({ title: "已成功回報", color: "success" });
    showReportModal.value = false;
    reportDesc.value = "";
  } catch (err) {
    toast.add({ title: "回報失敗", color: "error" });
  } finally {
    isReporting.value = false;
  }
};

const submitEdit = async () => {
  if (!editToilet.value) return;
  try {
    const res = await fetch(`${BASE_URL}/toilets/${editToilet.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title: editTitle.value }),
    });

    if (!res.ok) throw new Error("編輯失敗");

    toast.add({ title: "廁所名稱已更新", color: "success" });

    // 立即更新原本列表內的名稱（local update）
    const target = props.toilets.find((t) => t.id === editToilet.value?.id);
    if (target) target.title = editTitle.value;

    editToilet.value = null;
    editTitle.value = "";
  } catch (err) {
    toast.add({ title: "編輯失敗", color: "error" });
  }
};

const selectedAmenities = ref<Amenity["id"][]>([]);

const handleToggle = (id: number, checked: boolean) => {
  if (checked) {
    selectedAmenities.value.push(id);
  } else {
    selectedAmenities.value = selectedAmenities.value.filter((i) => i !== id);
  }
};
const newAmenityName = ref("");
const isAddingAmenity = ref(false);

const addAmenity = async () => {
  const name = newAmenityName.value.trim();
  if (!name) return;

  isAddingAmenity.value = true;
  try {
    const res = await fetch(`${BASE_URL}/amenities/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // ✅ Clerk JWT
      },
      body: JSON.stringify({ name }),
    });

    if (!res.ok) throw new Error("新增失敗");

    toast.add({ title: "備品已新增", color: "success" });
    newAmenityName.value = "";

    // ⏬ 重新載入備品資料
    if (reportToilet.value?.id) {
      await fetchAmenityData(reportToilet.value.id);
    }
  } catch (err) {
    toast.add({ title: "新增失敗", color: "error" });
  } finally {
    isAddingAmenity.value = false;
  }
};
</script>

<template>
  <div class="space-y-3">
    <UCard
      v-for="(toilet, index) in toilets"
      :key="index"
      class="border border-gray-200 dark:border-gray-700 p-4"
      @click="emit('select', toilet)"
    >
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-base font-bold">
          {{ toilet.title || "無名稱" }}
        </h3>
        <UIcon
          :name="
            'i-custom-' +
            toilet.type +
            (colorMode.value === 'dark' ? '-dark' : '')
          "
          class="size-8"
          mode="svg"
        />
      </div>

      <div class="flex items-center space-x-4 text-sm text-red-500">
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-star-solid" />
          <span>
            {{
              stats[toilet.id]?.avg_rating
                ? stats[toilet.id].avg_rating.toFixed(1)
                : "尚無評分"
            }}
          </span>
        </div>
        <div class="flex items-center space-x-1">
          <UIcon name="i-heroicons-chat-bubble-left-right" />
          <span>{{ stats[toilet.id]?.count || 0 }} 則</span>
        </div>

        <UButton
          v-if="!isLoading"
          :label="favorites.has(toilet.id) ? '已加入' : '我的最愛'"
          :color="favorites.has(toilet.id) ? 'success' : 'error'"
          variant="soft"
          icon="i-heroicons-heart"
          size="xs"
          @click.stop="toggleFavorite(toilet.id)"
        />

        <UButton v-else loading variant="soft" color="neutral" size="xs" />
        <UButton
          icon="i-heroicons-exclamation-triangle"
          size="xs"
          variant="soft"
          color="warning"
          @click.stop="
            reportToilet = toilet;
            showReportModal = true;
          "
        >
          回報問題
        </UButton>

        <UButton
          icon="i-heroicons-pencil-square"
          size="xs"
          variant="soft"
          color="primary"
          :disabled="!isAdmin"
          @click.stop="
            editToilet = toilet;
            editTitle = toilet.title || '';
          "
        >
          編輯
        </UButton>
      </div>
    </UCard>

    <p v-if="toilets.length === 0" class="text-center text-gray-400">
      🚽 查無廁所資訊
    </p>
  </div>
  <UModal v-model:open="showReportModal">
    <template #content>
      <div class="p-4 space-y-4">
        <UTabs
          v-model="selectedTab"
          :items="[
            { label: '我要回報', value: 'report' },
            { label: '備品管理', value: 'amenity', disabled: !isAdmin },
          ]"
        />

        <!-- Tab: 回報 -->
        <div v-if="selectedTab === 'report'" class="space-y-3">
          <h2 class="text-lg font-bold">
            回報問題：{{ reportToilet?.title || "（無名稱）" }}
          </h2>
          <UTextarea
            v-model="reportDesc"
            placeholder="請輸入問題描述，例如設備壞掉、無法使用等"
            autoresize
            class="w-full"
          />
          <div class="flex justify-end gap-2">
            <UButton
              color="neutral"
              variant="ghost"
              @click="showReportModal = false"
            >
              取消
            </UButton>
            <UButton color="primary" @click="submitReport">送出回報</UButton>
          </div>
        </div>

        <!-- Tab: 備品管理 -->
        <div v-if="selectedTab === 'amenity'" class="space-y-3">
          <h2 class="text-lg font-bold">備品管理</h2>

          <!-- 新增備品欄位 -->
          <div class="flex items-center gap-2">
            <UInput
              v-model="newAmenityName"
              placeholder="輸入備品名稱"
              class="flex-1"
            />
            <UButton
              color="primary"
              :loading="isAddingAmenity"
              @click="addAmenity"
            >
              新增
            </UButton>
          </div>

          <!-- 備品勾選列表 -->
          <UCheckbox
            v-for="item in allAmenities"
            :key="item.id"
            :label="item.name"
            :model-value="selectedAmenities.includes(item.id)"
            @update:model-value="handleToggle(item.id, $event as boolean)"
          />

          <div class="flex justify-end pt-2">
            <UButton color="primary" @click="saveAmenities">儲存</UButton>
          </div>
        </div>
      </div>
    </template>
  </UModal>

  <UModal v-model:open="isEditing">
    <template #content>
      <div class="p-4 space-y-3">
        <h2 class="text-lg font-bold">編輯廁所名稱</h2>
        <UInput
          v-model="editTitle"
          placeholder="請輸入新的名稱"
          class="w-full"
        />
        <div class="flex justify-end gap-2">
          <UButton color="neutral" variant="ghost" @click="editToilet = null">
            取消
          </UButton>
          <UButton color="primary" @click="submitEdit">儲存</UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>
