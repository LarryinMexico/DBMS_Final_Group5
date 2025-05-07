# 📁 專案結構

```text
.
├── README.md                          # 📘 專案說明文件
├── app.vue                            # 📲 Nuxt 預設入口，可自訂 layout 或 meta
├── assets                             # 🎨 靜態資源（不會被 Webpack 轉譯）
│   └── css
│       └── tailwind.css              # Tailwind CSS 主樣式匯入檔
├── components                         # 🧩 Vue 元件
│   ├── TheHeader                      # 頁首元件資料夾
│   │   ├── ColorModeButton.vue       # 切換深/淺色模式按鈕
│   │   └── index.vue                 # Header 主元件
│   └── TheMap                         # 地圖顯示元件資料夾
│       └── index.vue                 # 地圖主元件
├── constants
│   └── index.js                      # 📦 常數/環境變數定義（如 API URL）
├── nuxt.config.ts                    # ⚙️ Nuxt 設定檔（包含 module、plugin 等）
├── package-lock.json                 # 🔒 npm 鎖定檔，記錄精確套件版本
├── package.json                      # 📦 套件管理與 script 定義
├── pages
│   └── index.vue                     # 🏠 頁面主入口（自動路由為 `/`）
├── server
│   └── tsconfig.json                 # Server 專用 TypeScript 設定檔（若有 server function）
├── tsconfig.json                     # TypeScript 設定檔（整體專案使用）
└── utils
    └── useUserRegister.js           # 🪄 自動註冊 Clerk 使用者的 Composable（已登入自動發送 API）
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
   import MyComponent from "@/components/MyComponent/index.vue";
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
