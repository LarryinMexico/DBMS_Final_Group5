import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_interval=25,  # 每 25 秒發 ping，讓 Cloud Run 不殺連線
    ping_timeout=60,
)

