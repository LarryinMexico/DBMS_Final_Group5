# DBMS_Final_Group5

```text
DBMS_Final_Group5/
├── Frontend/               # Nuxt + NuxtUI 前端專案
│   ├── app/                # Nuxt 3 App 目錄結構
│   ├── components/         # UI 組件（整合 NuxtUI）
│   ├── pages/              # 路由頁面
│   ├── public/             # 靜態資源（錯誤圖示、地圖圖例）
│   ├── nuxt.config.ts      # Nuxt 設定檔
│   └── package.json        # 前端依賴與腳本
│
├── Backend/               # FastAPI 後端專案
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 資料模型（SQLAlchemy）
│   │   ├── schemas/        # Pydantic 資料結構
│   │   ├── services/       # 商業邏輯（CRUD、Redis）
│   │   ├── core/           # 設定檔、JWT 驗證邏輯
│   │   └── main.py         # FastAPI app 啟動點
│   ├── requirements.txt    # Python 依賴
│   └── Dockerfile          # FastAPI Docker 配置
│
├── README.md              # 專案介紹與啟動指南（含部署方式）

```
