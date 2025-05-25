# app/main.py
import uvicorn
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, toilet, building, favorite, review, reaction, amenity, report, follow, search
from app.socketio import sio

# 原始 FastAPI app
fastapi_app = FastAPI(root_path="/api")

# 註冊 API 路由
fastapi_app.include_router(user.router, prefix="/users", tags=["Users"])
fastapi_app.include_router(toilet.router, prefix="/toilets", tags=["Toilets"])
fastapi_app.include_router(building.router, prefix="/buildings", tags=["Buildings"])
fastapi_app.include_router(favorite.router, prefix="/favorites", tags=["Favorites"])
fastapi_app.include_router(review.router, prefix="/reviews", tags=["Reviews"])
fastapi_app.include_router(reaction.router, prefix="/reactions", tags=["Reactions"])
fastapi_app.include_router(amenity.router, prefix="/amenities", tags=["Amenities"])
fastapi_app.include_router(report.router, prefix="/reports", tags=["Reports"])
fastapi_app.include_router(follow.router, prefix="/follows", tags=["Follows"])
fastapi_app.include_router(search.router, prefix="/search", tags=["Search"])

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/")
def root():
    return {"message": "Welcome to Toilet Map API 🧻"}

# 🚀 用 SocketIO 包住 FastAPI app，這裡才是 final app
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

import logging

logging.basicConfig(level=logging.DEBUG)

@fastapi_app.middleware("http")
async def catch_all(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print("🔥 捕獲錯誤:", e)
        raise


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
