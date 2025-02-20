<details><summary>
GitHubの使い方
</summary><div>

```
# 最初だけ
git init
git branch -M main
git remote add origin https://github.com/sbmtrntr/Hackathon_team4.git
```

1. ローカルでmainブランチに移動
```bash
git checkout main
```

2. 最新のリモートリポジトリをpullする
```bash
git pull origin main
```

3. ローカルのmainブランチから、新しくブランチを作成する
```bash
git switch -c <ブランチ名>
```

4. 新しいブランチでファイルを更新した後、addしてcommitする
```bash
git add ファイル名 or .ですべてのファイル
git commit -m "<やったこと>"
```

5. リモートにpushする
```bash
git push origin <ブランチ名>
```

6. ブラウザのGithubでpull requestを作成する

</div></details>