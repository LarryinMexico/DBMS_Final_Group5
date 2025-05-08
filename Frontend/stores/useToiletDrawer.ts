import { defineStore } from 'pinia';

export const useToiletDrawer = defineStore('toiletDrawer', () => {
  const isOpen = ref(false);
  const toiletId = ref<number | null>(null);

  const open = (id: number) => {
    toiletId.value = id;
    isOpen.value = true;
  };

  const close = () => {
    isOpen.value = false;
    toiletId.value = null;
  };

  return {
    isOpen,
    toiletId,
    open,
    close,
  };
});
