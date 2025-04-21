<script setup>
import { ref, computed } from 'vue'
import { z } from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

const isOpen = ref(false)
const isSubmitting = ref(false)

const buildingOptions = [
  { label: '商學院', value: 'commerce' },
  { label: '達賢圖書館', value: 'library' },
]

const typeOptions = [
  { label: '男廁', value: 'male' },
  { label: '女廁', value: 'female' },
  { label: '性別友善廁所', value: 'unisex' },
  { label: '無障礙廁所', value: 'accessible' },
]

const toiletSchema = toTypedSchema(
  z.object({
    building: z.string({ required_error: '請選擇建築物' }),
    type: z.string({ required_error: '請選擇廁所類型' }),
    floor: z.string({ required_error: '請選擇樓層' }),
    name: z.string().optional(),
  })
)

const { handleSubmit, errors, defineField, values } = useForm({
  validationSchema: toiletSchema,
})

const [building, buildingAttrs] = defineField('building')
const [type, typeAttrs] = defineField('type')
const [floor, floorAttrs] = defineField('floor')
const [name, nameAttrs] = defineField('name')

const floorOptions = computed(() => {
  const count = (() => {
    if (!values.building) return 0
    switch (values.building.value) {
      case 'commerce':
        return 12
      case 'library':
        return 8
      default:
        return 0
    }
  })()
  return Array.from({ length: count }, (_, i) => ({
    label: `${i + 1} 樓`,
    value: `${i + 1}`,
  }))
})

const isSubmitDisabled = computed(() => {
  return (
    !values.building ||
    !values.type ||
    !values.floor ||
    isSubmitting.value
  )
})

async function onSubmit(values) {
  isSubmitting.value = true
  try {
    console.log('新增廁所資訊', values.building)
    // TODO: 呼叫 API 建立廁所
    // Set time out for 1 second to simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))
  } catch (error) {
    // TODO: 顯示錯誤通知
  } finally {
    const toast = useToast()    
    toast.add({
        title: 'Success',
        description: 'Your action was completed successfully.',
        color: 'success'
    })
    // Reset the form and close the modal
    handleSubmit(() => {
      // Reset the form values
      building.value = ''
      type.value = ''
      floor.value = ''
      name.value = ''
    })()
    isOpen.value = false
    isSubmitting.value = false
  }
}
</script>

<template>
    <div>
      <USlideover
        v-model:open="isOpen"
        :title="`新增廁所資訊 ${values.building ? ` @${values.building.label}` : ''}${values.floor ? ` -${values.floor.label}` : ''}`"
      >
      <UButton icon="i-lucide-plus" color="green" variant="solid">
        新增廁所
      </UButton>
        <template #body>
            <div class="flex flex-col h-full justify-start gap-y-10">
            <!-- 地點來源 -->
            <UCard>
              <template #header>
                <h2 class="text-base font-bold">地點資訊</h2>
              </template>
              <template #default>
                <URadioGroup
                  label="地點來源"
                  :items="[
                    { label: '選擇現有建築', value: 'building' },
                    { label: '自行輸入位置（尚未支援）', value: 'custom', disabled: true },
                  ]"
                  model-value="building"
                  disabled
                />
                <div class="flex flex-row justify-between py-5 space-x-2">
  
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
                  :loading="!values.building"
                  class="w-1/2"
                />
            </div>
              </template>
            </UCard>
  
            <!-- 廁所資訊 -->
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
  
                <UInput
                  label="名稱（選填）"
                  placeholder="例如：靠近電梯的廁所"
                  v-model="name"
                  v-bind="nameAttrs"
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
  