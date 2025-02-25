import os
from dotenv import load_dotenv

# ローカル環境なら .env.local を読み込む
if os.getenv("GAE_ENV") is None: # Cloud Run 環境では GAE_ENV が設定される
    load_dotenv("../.env.local")

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")