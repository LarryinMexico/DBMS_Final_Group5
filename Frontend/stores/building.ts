// stores/building.ts
import { defineStore } from "pinia";
import { ref } from "vue";
import { BASE_URL } from "@/constants";

export const useBuildingStore = defineStore("building", () => {
  const buildings = ref<any[]>([]);

  async function fetchBuildings() {
    const res = await fetch(`${BASE_URL}/buildings/`);
    buildings.value = await res.json();
  }

  async function addBuilding(newBuilding: any) {
    await fetchBuildings(); // 新增後自動更新列表
  }

  return { buildings, fetchBuildings, addBuilding };
});
