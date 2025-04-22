<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

const props = defineProps({
    toilets: {
        type: Array as () => Array<{
            floor: string | number
            type: string
            title?: string
        }>,
        default: () => []
    },
    buildingName: {
        type: String,
        default: ''
    }
})

// UBadge 可由外層統一註冊 Nuxt UI plugin 使用，不需要 resolveComponent
const columns: TableColumn<{ floor: string | number; type: string; title?: string }>[] = [
    {
        accessorKey: 'floor',
        header: '樓層'
    },
    {
        accessorKey: 'type',
        header: '類型',
        cell: ({ row }) =>
            row.getValue('type')
    },
    {
        accessorKey: 'title',
        header: '名稱',
        cell: ({ row }) => row.getValue('title') || '-'
    }
]
</script>

<template>
    <UCard class="w-full">
        <template #header>
            <h2 class="text-base font-bold">{{ buildingName || '廁所列表' }}</h2>
        </template>

        <UTable :data="toilets" :columns="columns" :striped="true" :hoverable="true" class="text-sm">
            <template #empty>
                <div class="text-center text-gray-500">無廁所資訊</div>
            </template>
        </UTable>
    </UCard>
</template>
