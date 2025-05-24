<!-- UserProfilePanel.vue -->
<script setup lang="ts">
import { BASE_URL } from "@/constants";
import ProfileReview from "./ProfileReview.vue";
import ProfileFavorites from "./ProfileFavorites.vue";

const props = defineProps<{ userId: string }>();

const reviews = ref([]);
const isLoading = ref(true);
const activeTab = ref(0);
const toast = useToast();

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

const userInfo = ref<{ name: string; avatarUrl: string } | null>(null);
const followersCount = ref(0);
const followingCount = ref(0);

onMounted(async () => {
  if (!props.userId) return;
  await checkFollowing();


  try {
    const [userRes, reviewRes, followersRes, followingRes] = await Promise.all([
      fetch(`${BASE_URL}/users/${props.userId}`),
      fetch(`${BASE_URL}/reviews/user/${props.userId}`),
      fetch(`${BASE_URL}/follows/followers/${props.userId}`),
      fetch(`${BASE_URL}/follows/following/${props.userId}`),
    ]);

    if (userRes.ok) userInfo.value = await userRes.json();
    if (reviewRes.ok) reviews.value = await reviewRes.json();
    if (followersRes.ok) followersCount.value = (await followersRes.json()).length;
    if (followingRes.ok) followingCount.value = (await followingRes.json()).length;
  } catch (err) {
    console.error("❌ 載入失敗", err);
  } finally {
    isLoading.value = false;
  }
});

const userStore = useUserStore();
const isFollowing = ref(false);

// 確認是否追蹤中
const checkFollowing = async () => {
  if (!userStore.id || !props.userId || userStore.id === +props.userId) return;

  try {
    const res = await fetch(`${BASE_URL}/follows/following/${userStore.id}`);
    const data = await res.json();
    isFollowing.value = data.some((u: any) => u.followed_id === +props.userId);
  } catch (err) {
    console.error("❌ 追蹤狀態取得失敗", err);
  }
};

const toggleFollow = async () => {
  const me = userStore.id;
  const target = +props.userId;
  if (!me || !target) return;

  const method = isFollowing.value ? "DELETE" : "POST";
  const url = isFollowing.value
    ? `${BASE_URL}/follows/${me}/${target}`
    : `${BASE_URL}/follows/`;

  const body = isFollowing.value
    ? undefined
    : JSON.stringify({ following_id: me, followed_id: target });

  try {
    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body,
    });

    if (!res.ok) throw new Error("追蹤操作失敗");

    isFollowing.value = !isFollowing.value;

    // ✅ 同步更新粉絲數（只有在觀看他人 profile 時才生效）
    if (+props.userId !== userStore.id) {
      followersCount.value += isFollowing.value ? 1 : -1;
    }

    toast.add({
      title: isFollowing.value ? "已追蹤" : "已取消追蹤",
      color: "success",
    });
  } catch (err) {
    toast.add({ title: "操作失敗", color: "error" });
  }
};

import { useSocket } from "@/utils/useSocket";

const { joinRoom } = useSocket();

onMounted(() => {
  joinRoom(); // 🔔 加入自己的房間
});


</script>

<template>
  <div class="space-y-4 p-6">
    <!-- 頭像與簡介 -->
    <div class="flex flex-row items-center gap-4 justify-between ">
    <div class="flex items-center gap-4">
      <UAvatar :src="userInfo?.avatarUrl" :alt="userInfo?.name" size="lg" />
      <div>
        <h2 class="text-lg font-bold">{{ userInfo?.name ?? '匿名使用者' }}</h2>
        <p class="text-sm text-gray-500">
          {{ reviews.length }} 則評論・{{ followingCount }} 追蹤中・{{ followersCount }} 粉絲
        </p>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <!-- 若瀏覽的不是自己，顯示追蹤按鈕 -->
      <UButton v-if="userStore.id && +props.userId !== userStore.id" :color="isFollowing ? 'primary' : 'neutral'"
        variant="soft" size="lg" icon="i-heroicons-user-plus" @click="toggleFollow">
        {{ isFollowing ? '已追蹤' : '追蹤' }}
      </UButton>
      </div>
    </div>

    <UTabs v-model="activeTab" :items="[{ label: '最愛' }, { label: '評論' }, { label: '統計' }]">
      <template #content="{ item }">
        <div v-if="isLoading" class="text-sm text-gray-500 py-4">載入中...</div>
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
