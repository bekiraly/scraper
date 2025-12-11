from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router

app = FastAPI()

@app.get("/debug/apikey")
def debug_key():
    return {"API_FOOTBALL_KEY": os.getenv("API_FOOTBALL_KEY")}

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router bağlama
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "NewDayAI Engine"}

