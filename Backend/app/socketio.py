import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["*"],  # ✅ 若未設，會被 Cloud Run 擋掉
    ping_interval=25,
    ping_timeout=60,
)


