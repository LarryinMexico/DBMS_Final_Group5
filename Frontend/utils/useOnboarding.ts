// composables/useHeaderTour.ts
import Shepherd from "shepherd.js";

export const useOnboarding = () => {
  const tour = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
      scrollTo: true,
      cancelIcon: { enabled: true },
      classes:
        "shadow-md bg-white dark:bg-gray-900 text-gray-800 dark:text-white",
    },
  });

  tour.addStep({
    id: "filter",
    text: "點這裡可以打開廁所篩選器，根據樓層、評價或設備篩選。",
    attachTo: {
      element: ".filter-btn",
      on: "bottom",
    },
    buttons: [{ text: "下一步", action: tour.next }],
  });

  tour.addStep({
    id: "location",
    text: "這裡可以啟用即時定位功能，追蹤你的 GPS 位置。",
    attachTo: {
      element: ".locate-btn",
      on: "bottom",
    },
    buttons: [
      { text: "返回", action: tour.back },
      { text: "下一步", action: tour.next },
    ],
  });

  tour.addStep({
    id: "toilet-icon",
    text: "地圖上的圖示代表一棟建築物，點擊即可查看廁所。",
    attachTo: {
      element: ".building-marker", // 👈 你要給建築 icon 加這個 class
      on: "top",
    },
    buttons: [
      { text: "返回", action: tour.back },
      { text: "下一步", action: tour.next },
    ],
  });

  tour.addStep({
    id: "profile",
    text: "點擊這裡可以開啟你的個人頁面，檢視最愛、評論與統計資料。",
    attachTo: {
      element: ".profile-btn",
      on: "bottom",
    },
    buttons: [
      { text: "返回", action: tour.back },
      { text: "完成", action: tour.complete },
    ],
  });

  return { startTour: () => tour.start() };
};
