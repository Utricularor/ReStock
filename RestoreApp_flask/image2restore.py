import glob
import os
import json

from StockManager import StockManager
from TextExtracter import TextExtracter

def pipe():
    # 画像・テキストパス設定
    image_dir = 'uploads/'
    text_dir = 'output/'

    image_path = os.listdir(image_dir)
    print(image_path)

    # OCR
    if image_path:
        text_extractor = TextExtracter(image_dir+image_path[0], text_dir)
        text_extractor.extract_text()

    # Summarize
    text_path = os.listdir(text_dir)
    print(text_path)
    if text_path:
        summarized_data_json = text_extractor.summarize_text()
        summarized_data_dict = json.loads(summarized_data_json)
        print(summarized_data_dict)

    # DB追加
    stock_manager = StockManager()
    stock_manager.insert_at_once(summarized_data_dict)