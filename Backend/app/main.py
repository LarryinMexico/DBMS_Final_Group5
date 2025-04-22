# app/main.py
from fastapi import FastAPI
from app.routers import user, toilet, building, favorite
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api")
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(toilet.router, prefix="/toilets", tags=["Toilets"])
app.include_router(building.router, prefix="/buildings", tags=["Buildings"])
app.include_router(favorite.router, prefix="/favorites", tags=["Favorites"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端 origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Toilet Map API 🧻"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
