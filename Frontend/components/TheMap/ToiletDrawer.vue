<script setup lang="ts">
import { ref, watch } from 'vue'
import ToiletCardList from './ToiletCardList.vue'
import ToiletDetail from './ToiletDetail.vue'

const props = defineProps<{
  buildingName: string
  toilets: Array<{ id: string; floor: string | number; type: string; title?: string }>
  isOpen: boolean
}>()

const emit = defineEmits(['close'])

const localOpen = ref(props.isOpen)
const selectedToilet = ref<typeof props.toilets[0] | null>(null)

watch(() => props.isOpen, val => {
  localOpen.value = val
})

// 回到列表
function backToList() {
  selectedToilet.value = null
}
</script>


<template>
    <UDrawer v-model="localOpen" direction="left" @close="emit('close')">
      <template #header>
        <div class="flex justify-between items-center px-4 py-2">
          <h2 class="text-lg font-bold truncate">
            {{ selectedToilet ? selectedToilet.title || '廁所詳情' : buildingName }}
          </h2>
          <UButton icon="i-lucide-x" variant="ghost" @click="emit('close')" />
        </div>
      </template>
  
      <template #body>
        <div class="p-4 min-w-[350px] space-y-4 overflow-y-auto">
          <!-- 列表頁面 -->
          <ToiletCardList
            v-if="!selectedToilet"
            :toilets="toilets"
            @select="(toilet) => (selectedToilet = toilet)"
          />
  
          <!-- 詳細頁面 -->
          <ToiletDetail
            v-else
            :toilet="selectedToilet"
            @back="backToList"
          />
        </div>
      </template>
    </UDrawer>
  </template>
  