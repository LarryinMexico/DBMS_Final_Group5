# app/socketio.py
import json
from app.db.redis import redis_client
from socketio import AsyncServer
from sqlalchemy.orm import Session
from app.models import user as models
from app.db.session import get_db

sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")

@sio.on("update-location")
async def handle_update_location(sid, data):
    """
    接收前端傳來的 user_id、lat、lng、avatarUrl、name
    """
    try:
        # 確保資料格式正確
        user_id = data["user_id"]
        lat = data["lat"]
        lng = data["lng"]

        key = f"location:{user_id}"

        # Get the database session
        db: Session = next(get_db())
        user = db.query(models.User).filter(models.User.id == user_id).first()

        payload = {
            "lat": lat,
            "lng": lng,
            "name": user.name,
            "avatarUrl": user.avatarUrl,
        }

        # ✅ 存進 Redis，並設 TTL（例如 60 秒）
        await redis_client.set(key, json.dumps(payload), ex=60)

        # ✅ 廣播給其他人
        await sio.emit("location-updated", {
            "user_id": user_id,
            "location": {
                "lat": lat,
                "lng": lng,
                "avatarUrl": user.avatarUrl,
                "name": user.name,
            },
        }, skip_sid=sid)

    except Exception as e:
        print("❌ Failed to update location:", e)