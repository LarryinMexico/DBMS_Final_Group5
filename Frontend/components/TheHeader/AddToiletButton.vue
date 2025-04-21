<script setup>
import { ref, computed } from 'vue'
import { z } from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import ToiletMapSelector from '@/components/TheHeader/ToiletMapSelector.vue'
import { reverseGeocode } from '@/utils/reverseGeocode.js'

const isOpen = ref(false)
const isSubmitting = ref(false)
const location = ref({ lng:121.5773869, lat:24.9878484 })
const locationSource = ref('building')
const address = reverseGeocode(location.value.lng, location.value.lat)

watch(location, async (newLocation) => {
  if (locationSource.value === 'custom') {
    console.log('Custom location selected:', newLocation)
    address.value = await reverseGeocode(newLocation)
    buildingName.value = address.value
  }
})


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
    building: z.string().optional(),
    buildingName: z.string().optional(),
    floorMin: z.string().optional(),
    floorMax: z.string().optional(),
    floor: z.string({ required_error: '請選擇樓層' }),
    type: z.string({ required_error: '請選擇廁所類型' }),
    name: z.string().optional(),
  })
)

const { handleSubmit, errors, defineField, values } = useForm({
  validationSchema: toiletSchema,
})

const [building, buildingAttrs] = defineField('building')
const [buildingName, buildingNameAttrs] = defineField('buildingName')
const [floorMin, floorMinAttrs] = defineField('floorMin')
const [floorMax, floorMaxAttrs] = defineField('floorMax')
const [floor, floorAttrs] = defineField('floor')
const [type, typeAttrs] = defineField('type')
const [name, nameAttrs] = defineField('name')

const floorOptions = computed(() => {
  const count = (() => {
    if (locationSource.value === 'building') {
      switch (values.building?.value) {
        case 'commerce': return 12
        case 'library': return 8
        default: return 0
      }
    }
    if (values.floorMax) {
      return Number(values.floorMax) || 0
    }
    return 0
  })()
  return Array.from({ length: count }, (_, i) => ({
    label: `${i + 1} 樓`,
    value: `${i + 1}`,
  }))
})

const isSubmitDisabled = computed(() => {
  return (
    !values.floor ||
    !values.type ||
    isSubmitting.value
  )
})

async function onSubmit(values) {
  isSubmitting.value = true
  try {
    console.log('新增廁所資訊', values, location.value)
    await new Promise((resolve) => setTimeout(resolve, 1000))
  } catch (error) {
    console.error(error)
  } finally {
    const toast = useToast()
    toast.add({
      title: 'Success',
      description: '成功新增廁所資訊',
      color: 'success'
    })
    isOpen.value = false
    isSubmitting.value = false
  }
}
</script>

<template>
  <div>
    <USlideover v-model:open="isOpen" title="新增廁所資訊">
    <UButton icon="i-lucide-plus" color="green" variant="solid" @click="isOpen = true">
      新增廁所
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

              <div v-if="locationSource === 'building'" class="flex flex-row justify-between py-5 space-x-2">
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
                <UFormField label="最低樓層" required>
                  <UInput type="number" v-model="floorMin" v-bind="floorMinAttrs" class="w-full" />
                </UFormField>
                <UFormField label="最高樓層" required>
                  <UInput type="number" v-model="floorMax" v-bind="floorMaxAttrs" class="w-full" />
                </UFormField>
                </div>

                <div class="flex gap-2">
                <UFormField label="建築名稱" required class="w-full">
                    <UInput class="w-full" v-model="buildingName" v-bind="buildingNameAttrs" />
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
                <ToiletMapSelector v-model="location" class="mt-2 rounded overflow-hidden h-72" />
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