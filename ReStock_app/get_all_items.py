import json
from StockManager import StockManager

def get_all_items():
    stockmanager = StockManager()
    all_items_json = stockmanager.get_all_items()
    all_items_json = all_items_json.encode().decode('unicode-escape')
    data = json.loads(all_items_json)
    return data['明細']

if __name__ == "__main__":
    print(get_all_items())