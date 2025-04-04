# 📁 專案結構

```text
.
├── README.md
├── app.vue
├── assets
│   └── css
│       └── tailwind.css
├── components
│   ├── TheHeader
│   │   ├── ColorModeButton.vue
│   │   └── index.vue
│   └── TheMap
│       └── index.vue
├── nuxt.config.ts
├── package-lock.json
├── package.json
├── pages
│   └── index.vue
├── public
│   ├── favicon.ico
│   └── robots.txt
├── server
│   └── tsconfig.json
└── tsconfig.json
```

## 🧪 開發與啟動方式

1. 安裝相依套件：

   ```bash
   npm install
   ```

2. 啟動開發伺服器：

   ```bash
   npm run dev
   ```

## 🧭 開發指引（如何加入新元件）

若你想要加入新的元件或頁面，可依循以下步驟操作：

### 新增元件

1. 建立新的元件檔案至 `components/` 目錄下，建議採用資料夾包裝的方式：

   ```text
   components/
   └── MyComponent/
       ├── index.vue
       └── MyComponentUtils.ts
   ```

2. 在需要的頁面或父元件中引入並使用：

   ```vue
   <script setup>
   import MyComponent from '@/components/MyComponent/index.vue'
   </script>

   <template>
     <MyComponent />
   </template>
   ```

### 串接 API

1. 建議集中處理 API 函式在 `utils/api/` 或 `composables/useApi.ts` 中
2. 請使用 `.env` 檔設定 API base URL，例如： (部署中)

   ```text
   API_URL=https://toilet-map-api-xyz.a.run.app
   ```

3. 使用 `useFetch` 或 `useAsyncData` 進行資料取得

## 🛠 技術棧

- **框架**：Nuxt 3
- **樣式**：Tailwind CSS
- **地圖**：Mapbox GL JS
- **認證**：Clerk
- **部署**：Vercel
