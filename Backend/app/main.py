# app/main.py
from fastapi import FastAPI
from app.routers import user
import uvicorn

app = FastAPI()
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to Toilet Map API 🧻"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
