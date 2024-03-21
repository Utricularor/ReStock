# ReStock
ReStockは買い物の際に家に何があるのかを一目でわかるようにし、重複した買い物をなくすためのアプリです。

「帰り道に買い物に行こうと思ったけど、家に何があったか忘れた…」なんて経験はありませんか？
そういった場合でも ReStock があればその問題を解決できます。

## 使用例
### レシートの画像 (公開用として一部のみの画像を使用してます。)
<img src="https://github.com/Utricularor/ReStock/assets/75835652/c25e198a-6cec-4223-9b83-68db5595a9d2" width=200>

### 画像をアップロードすると、家にあるものリストに商品が追加される
家にあるものリストから削除すると、家にないものリストに追加されるため、次回の買い物時に何を買うべきかが一目瞭然。  
また、手動での追加、品名の名前や数の修正もできます。同じ商品が追加された場合は、追加の数だけ増えます。
<img src="https://github.com/Utricularor/ReStock/assets/75835652/68a34030-f29b-41f0-b1bd-d22d4ad66c06" width=1000 >

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

## デプロイ方法
[こちら](https://learn.microsoft.com/ja-jp/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli)のサイトを参考に簡単にインターネット上に公開することができます。
