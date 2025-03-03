# 1. ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. ローカルのファイルをコンテナにコピー
COPY . /app

# 4. 依存パッケージのインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# 5. UvicornでFastAPIを実行
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# メモ：docker build -t fastapi-app .でイメージをビルド
# メモ：docker run -d -p 8080:8080 fastapi-appでコンテナを起動