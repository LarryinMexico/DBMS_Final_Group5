<script setup lang="ts">
import { ref } from "vue";
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/user";

const props = defineProps<{ toiletId: number }>();
const emit = defineEmits<{ (e: "submitted"): void }>();

const rating = ref(0);
const hoverRating = ref(0);
const comment = ref("");
const toast = useToast();
const user = useUserStore();
const icons = Array.from({ length: 5 }, (_, i) => i + 1);

const submitReview = async () => {
  if (!user.id || rating.value === 0) return;

  try {
    const res = await fetch(`${BASE_URL}/reviews/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user.id,
        toilet_id: props.toiletId,
        rating: rating.value,
        comment: comment.value,
      }),
    });

    if (!res.ok) throw new Error("評論送出失敗");

    toast.add({ title: "評論送出成功", color: "success" });
    rating.value = 0;
    comment.value = "";
    emit("submitted");
  } catch (error) {
    toast.add({
      title: "評論送出失敗",
      description: "請稍後再試",
      color: "error",
    });
  }
};
</script>

<template>
  <div class="space-y-4">
    <!-- 使用者資訊 -->
    <div class="flex items-center space-x-3">
      <UAvatar size="md" :src="user.avatar" />
      <div>
        <p class="text-base font-bold">{{ user.name }}</p>
        <p class="text-xs text-gray-400">正在撰寫公開評論</p>
      </div>

      <!-- 評分區塊 -->
      <UIcon
        v-for="n in icons"
        :key="n"
        name="i-heroicons-star-solid"
        class="w-6 h-6 cursor-pointer transition-colors"
        :class="
          (hoverRating || rating) >= n
            ? 'text-yellow-400'
            : 'text-gray-400 hover:text-yellow-300'
        "
        @mouseenter="hoverRating = n"
        @mouseleave="hoverRating = 0"
        @click="rating = n"
      />
    </div>

    <!-- 評論輸入 -->
    <UTextarea
      v-model="comment"
      :maxrows="4"
      :autoresize="true"
      placeholder="詳細說明你在這個地點的親身體驗"
      class="w-full"
    />

    <!-- 送出按鈕 -->
    <div class="flex justify-end">
      <UButton
        label="送出評論"
        color="primary"
        size="sm"
        :disabled="!comment || rating === 0"
        @click="submitReview"
      />
    </div>
  </div>
</template>
