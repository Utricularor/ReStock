import os

from flask import Flask, render_template, request, redirect, url_for

import image2restore
from StockManager import StockManager

app = Flask(__name__)

# アップロードしたレシート画像を保存するディレクトリ
app.config['UPLOAD_FOLDER'] = 'uploads/'

# StockManagerインスタンス作成
stock_manager = StockManager()

@app.route("/", methods=['GET', 'POST'])
def index():
    # 開始時点での在庫を取得
    ingredients = stock_manager.get_all_items()
    deleted_items = stock_manager.get_deleted_items()

    if request.method == 'POST':
        if 'item_name' in request.form and 'item_quantity' in request.form:
            # 新しい食材を追加
            item_name = request.form['item_name']
            item_quantity = int(request.form['item_quantity'])
            stock_manager.insert_stock(item_name, item_quantity)
            ingredients = stock_manager.get_all_items()

        elif 'delete_item' in request.form:
            # 食材を削除
            item_name = request.form['delete_item_name']
            item_quantity = request.form['delete_item_quantity']
            stock_manager.delete_stock(item_name)
            ingredients = stock_manager.get_all_items()

            # DeletedStockを更新
            stock_manager.insert_to_deletedlist(item_name, item_quantity)
            deleted_items = stock_manager.get_deleted_items()
            
    # return render_template("index.html", ingredients=ingredients)  
    return render_template("index.html", ingredients=ingredients, deleted_items=deleted_items)

# アップロード処理用のルート
@app.route("/uploads", methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = 'recipt.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # 画像入力からデータベース追加
        image2restore.pipe()

    return redirect(url_for('index'))

@app.route("/edit", methods=['GET'])
def edit():
    if 'item_name' in request.args and 'item_quantity' in request.args:
        item_name = request.args['item_name']
        item_quantity = request.args['item_quantity']
        return render_template('edit.html', item_name=item_name, item_quantity=item_quantity)
    return redirect(url_for('index'))

@app.route("/modify", methods=['POST'])
def modify():
    if request.method == 'POST':
        if 'old_item_name' in request.form and 'new_item_name' in request.form and 'new_item_quantity' in request.form:
            # 古い情報の商品を削除
            old_item_name = request.form['old_item_name']
            stock_manager.delete_stock(old_item_name)

            # 新しい情報で商品を追加
            new_item_name = request.form['new_item_name']
            new_item_quantity = int(request.form['new_item_quantity'])
            stock_manager.insert_stock(new_item_name, new_item_quantity)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)