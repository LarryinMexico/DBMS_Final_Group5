# app/main.py
import socketio
from fastapi import FastAPI
from app.routers import user, toilet, building, favorite, review, reaction, amenity, report, follow
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
fastapi_app = FastAPI(root_path="/api")
socket_app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

app = fastapi_app
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(toilet.router, prefix="/toilets", tags=["Toilets"])
app.include_router(building.router, prefix="/buildings", tags=["Buildings"])
app.include_router(favorite.router, prefix="/favorites", tags=["Favorites"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])
app.include_router(reaction.router, prefix="/reactions", tags=["Reactions"])
app.include_router(amenity.router, prefix="/amenities", tags=["Amenities"])
app.include_router(report.router, prefix="/reports", tags=["Reports"])
app.include_router(follow.router, prefix="/follows", tags=["Follows"])

@sio.event
async def connect(sid, environ):
    print("✅ Connected:", sid)

@sio.event
async def disconnect(sid):
    print("❌ Disconnected:", sid)

@sio.event
async def join(sid, data):
    print(f"🎯 {sid} join room {data['room']}")
    await sio.enter_room(sid, data["room"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端 origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount the socket.io app
app.mount("/socket.io", socket_app)

@app.get("/")
def root():
    return {"message": "Welcome to Toilet Map API 🧻"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
