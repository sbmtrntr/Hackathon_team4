## Pythonの環境構築
1. python3.9をインストール

2. 以下モジュールをインストール

    `pip install supabase-py python-dotenv fastapi uvicorn`

3. このディレクトリ下に移動し、以下を実行

    `uvicorn main:app --host localhost --port 8080 --reload`

4. http://localhost:8080 でHello Worldが表示されていればOK