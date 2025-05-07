<script setup lang="ts">
import ReviewForm from "@/components/TheMap/Review/ReviewForm.vue";
import ReviewList from "@/components/TheMap/Review/ReviewList.vue";

const props = defineProps<{
  toilet: { id: number; floor: string | number; type: string; title?: string };
}>();

const reloadReviews = ref(0); // 可以透過切換這個觸發重新 fetch

const triggerReload = () => {
  reloadReviews.value++;
};
</script>

<template>
  <div class="space-y-4">
    <ReviewForm :toilet-id="props.toilet.id" @submitted="triggerReload" />
    <ReviewList :toilet-id="props.toilet.id" :reload="reloadReviews" />
  </div>
</template>
