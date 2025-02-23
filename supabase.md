1. Supabase クライアントを使うためにsupabase-jsをインストール
    ```bash
    npm install @supabase/supabase-js
    ```

2. Discordに載せた.env.localをプロジェクト直下に追加
   - この環境変数を用いてSupabaseのデータベースに接続する
   - このファイルはGitにあげてはいけないため、.gitignoreで無視されるようになっています

3. 適宜データベースからデータの取得・追加・削除処理を作成
   
   例）src/app/supabaseExample/page.tsx

   (http://localhost:3000/supabaseExample で確認できます)