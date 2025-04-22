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

// watch selectedToilet and log
watch(selectedToilet, (val) => {
  console.log('selectedToilet changed:', val)
})

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
      <div class="px-4 py-2">
        <div v-if="selectedToilet" class="relative flex items-center justify-between">
          <!-- 左：返回 -->
          <div>
            <UButton
              variant="ghost"
              icon="i-lucide-chevron-left"
              class="text-md text-gray-500 hover:text-gray-700"
              @click="backToList"
              label="返回"
            />
          </div>

          <!-- 中：標題（置中） -->
          <h2 class="absolute left-1/2 transform -translate-x-1/2 text-lg font-bold truncate">
            {{ selectedToilet.title || '廁所詳情' }}
          </h2>

          <!-- 右：關閉 -->
          <div>
            <UButton icon="i-lucide-x" variant="ghost" @click="emit('close')" />
          </div>
        </div>

        <div v-else class="flex items-center justify-between">
          <!-- 左：建築名稱 -->
          <h2 class="text-lg font-bold truncate">{{ buildingName }}</h2>

          <!-- 右：關閉 -->
          <UButton icon="i-lucide-x" variant="ghost" @click="emit('close')" />
        </div>
      </div>
    </template>


    <template #body>
      <div class="p-4 min-w-[350px] space-y-4 overflow-y-auto">
        <!-- 列表頁面 -->
        <ToiletCardList v-if="!selectedToilet" :toilets="toilets" @select="(toilet) => (selectedToilet = toilet)" />

        <!-- 詳細頁面 -->
        <ToiletDetail v-else :toilet="selectedToilet" />
      </div>
    </template>
  </UDrawer>
</template>
  