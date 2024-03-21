# ReStock
ReStockは買い物の際に家に何があるのかを一目でわかるようにし、重複した買い物をなくすためのアプリです。

「帰り道に買い物に行こうと思ったけど、家に何があったか忘れた…」なんて経験はありませんか？
そういった場合でも ReStock があればその問題を解決できます。

## 使用例
### レシートの画像 (公開用として一部編集してます。)
<img src="https://github.com/Utricularor/ReStock/assets/75835652/ca7a938e-2e3d-42ef-aa49-208ad0ebd96b" width=200>

### 画像をアップロードすると、在庫リストに商品が追加される（削除・手動での追加もできる）
<img src="https://github.com/Utricularor/ReStock/assets/75835652/8faff403-df59-4c8b-8e01-1b92c62ed281" width=1000 >

## 設定
設定は`.env`に記載します。
### .env
　以下の環境変数を設定します。

#### Azure Computer Vision
- `VISION_KEY`: Azure Computer Visionのキー
- `VISION_ENDPOINT`: Azure Computer Visionのエンドポイント

#### Azure SQL database
- `DATABASE_SERVER`:　データベースのサーバー名
- `DATABASE_NAME`:　データベースの名前
- `DATABASE_ADMIN_ID`:　データベース管理者のID
- `DATABASE_ADMIN_PASS`: データベース管理者のパスワード
- `DATABASE_DRIVER`: データベースのドライバー

#### OpenAI
- `OPENAI_KEY`: OpenAI API のキー

## 実行方法
以下のコマンドで、ローカルでアプリを起動することができます。

```bash
$ python app.py
```
