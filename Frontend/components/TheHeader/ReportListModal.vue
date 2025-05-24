<script setup lang="ts">
import { BASE_URL } from "@/constants";

const props = defineProps<{ open: boolean }>();
const emit = defineEmits<{
  (e: "close"): void;
}>();

const toast = useToast();

interface Report {
  id: number;
  toiletId: number;
  toiletTitle?: string;
  description: string;
  status: "pending" | "resolved" | "rejected";
  user_id: number;
  userInfo?: {
    name: string;
    avatarUrl: string;
  };
}

const reports = ref<Report[]>([]);

// 分頁邏輯
const currentPage = ref(1);
const perPage = 3; // 每頁顯示 5 筆
const pageCount = computed(() => Math.ceil(reports.value.length / perPage));

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * perPage;
  return reports.value.slice(start, start + perPage);
});

const statusColors: Record<Report["status"], "warning" | "success" | "error"> =
  {
    pending: "warning",
    resolved: "success",
    rejected: "error",
  };

const fetchReports = async () => {
  try {
    const res = await fetch(`${BASE_URL}/reports/`);
    const rawData = await res.json();

    const filled = await Promise.all(
      rawData.map(async (r: any) => {
        const [toiletRes, userRes] = await Promise.all([
          fetch(`${BASE_URL}/toilets/${r.toilet_id}`),
          fetch(`${BASE_URL}/users/4`),
        ]);
        const [toilet, user] = await Promise.all([
          toiletRes.json(),
          userRes.json(),
        ]);

        return {
          id: r.id,
          toiletId: r.toilet_id,
          user_id: r.user_id,
          description: r.description,
          status: r.status,
          toiletTitle: toilet.title ?? "（無名稱）",
          userInfo: {
            name: user.name,
            avatarUrl: user.avatarUrl,
          },
        } as Report;
      }),
    );

    reports.value = filled;
  } catch (err) {
    toast.add({ title: "讀取失敗", color: "error" });
  }
};

const updateStatus = async (id: number, status: Report["status"]) => {
  try {
    const res = await fetch(`${BASE_URL}/reports/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ id, status }),
    });
    if (!res.ok) throw new Error("更新失敗");
    toast.add({ title: "狀態已更新", color: "success" });
    const target = reports.value.find((r) => r.id === id);
    if (target) target.status = status; // 即時更新畫面
  } catch (err) {
    toast.add({ title: "更新失敗", color: "error" });
  }
};

watchEffect(() => {
  if (props.open) fetchReports();
});

const getItems = (reportId: number) => {
  return [
    {
      label: "🛠️ 待處理",
      value: "pending",
      async onSelect() {
        await updateStatus(reportId, "pending");
      },
    },
    {
      label: "✅ 已解決",
      value: "resolved",
      async onSelect() {
        await updateStatus(reportId, "resolved");
      },
    },
    {
      label: "❌ 已拒絕",
      value: "rejected",
      async onSelect() {
        await updateStatus(reportId, "rejected");
      },
    },
  ];
};
</script>

<template>
  <UModal :open="props.open" @close="emit('close')">
    <template #content>
      <div class="p-4 space-y-3">
        <h2 class="text-xl font-bold">🔧 報修列表</h2>

        <UCard v-for="r in paginatedReports" :key="r.id">
          <template #header>
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium text-base">
                  {{ r.toiletTitle }}
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <div class="text-xs text-gray-400">
                  回報者：{{ r.userInfo?.name || "未知使用者" }}
                </div>
                <UAvatar
                  v-if="r.userInfo?.avatarUrl"
                  :src="r.userInfo.avatarUrl"
                  :alt="r.userInfo.name"
                  size="sm"
                />
              </div>
            </div>
          </template>

          <div class="text-sm text-gray-500 mb-2">{{ r.description }}</div>

          <template #footer>
            <UDropdownMenu :items="getItems(r.id)">
              <UButton
                size="xs"
                :color="
                  statusColors[r.status as 'pending' | 'resolved' | 'rejected']
                "
                variant="soft"
              >
                {{
                  r.status === "pending"
                    ? "🛠️"
                    : r.status === "resolved"
                      ? "✅"
                      : "❌"
                }}
                {{ r.status }}
              </UButton>
            </UDropdownMenu>
          </template>
        </UCard>

        <!-- 分頁 -->
        <div class="flex justify-center pt-2">
          <UPagination
            v-model:page="currentPage"
            :items-per-page="pageCount"
            :total="reports.length"
          />
        </div>

        <UButton block @click="emit('close')">關閉</UButton>
      </div>
    </template>
  </UModal>
</template>
