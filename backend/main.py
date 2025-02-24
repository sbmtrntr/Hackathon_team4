from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import database, root

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加
app.include_router(root.router) # ルートに接続した時
app.include_router(database.router) # データベースに関する操作

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)