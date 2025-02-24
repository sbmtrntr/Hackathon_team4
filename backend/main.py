import os
from supabase import Client, create_client
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ローカル環境なら .env.local を読み込む
if os.getenv("GAE_ENV") is None:  # Cloud Run 環境では GAE_ENV が設定される
    load_dotenv("../.env.local")

URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

supabase: Client = create_client(URL, KEY)

app = FastAPI()

# CORS 設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（必要なら適宜変更）
    allow_credentials=True,
    allow_methods=["*"],  # すべての HTTP メソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user_name")
def read_user_name():
    response = supabase.table("users").select("name").execute()
    return response