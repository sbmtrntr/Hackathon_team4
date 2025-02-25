## Pythonの環境構築
1. python3.9をインストール

2. 以下モジュールをインストール

    `pip install -r requirements.txt`

3. このディレクトリ下に移動し、以下を実行

    `uvicorn main:app --host localhost --port 8080 --reload`

4. http://localhost:8080 でHello Worldが表示されていればOK


## データベース操作のAPI使用法
`uvicorn main:app --host localhost --port 8080 --reload`で起動させた状態で操作

コマンドラインではなく、ブラウザで http://localhost:8080/~~ にアクセスしてもOK
```bash
# 各テーブルの作成
curl -X POST http://localhost:8080/create-users
curl -X POST http://localhost:8080/create-user-attributes
curl -X POST http://localhost:8080/create-matching-history
curl -X POST http://localhost:8080/create-slack-channels

# 各テーブルの削除
curl -X POST http://localhost:8080/drop-users
curl -X POST http://localhost:8080/drop-user-attributes
curl -X POST http://localhost:8080/drop-matching-history
curl -X POST http://localhost:8080/drop-slack-channels

# 各テーブルに架空データを挿入
curl -X POST http://localhost:8080/insert-users
curl -X POST http://localhost:8080/insert-user-attributes
```

## データベースの表を確認したいとき
```bash
# usersテーブルの情報を取得
curl -X GET http://localhost:8080/users

# user_attributesテーブルの情報を取得
curl -X GET http://localhost:8080/user_attributes
```