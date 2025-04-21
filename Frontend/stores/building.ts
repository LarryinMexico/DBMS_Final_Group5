// stores/building.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { BASE_URL } from '@/constants'

export const useBuildingStore = defineStore('building', () => {
  const buildings = ref<any[]>([])

  async function fetchBuildings() {
    const res = await fetch(`${BASE_URL}/buildings/`)
    buildings.value = await res.json()
  }

  async function addBuilding(newBuilding: any) {
    const res = await fetch(`${BASE_URL}/buildings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newBuilding)
    })

    if (!res.ok) throw new Error('新增建築失敗')

    await fetchBuildings() // 新增後自動更新列表
  }

  return { buildings, fetchBuildings, addBuilding }
})
