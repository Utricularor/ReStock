from dotenv import dotenv_values
import pyodbc
import json

class StockManager():
    def __init__(self):
        self.config = dotenv_values(".env")
        DATABASE_SERVER = self.config["DATABASE_SERVER"]
        DATABASE_NAME = self.config["DATABASE_NAME"]
        DATABASE_USERNAME = self.config["DATABASE_ADMIN_ID"]
        DATABASE_PASSWORD = self.config["DATABASE_ADMIN_PASS"]
        DATABASE_DRIVER = self.config["DATABASE_DRIVER"]

        self.ODBC = 'DRIVER=' + DATABASE_DRIVER + \
                    ';SERVER=' + DATABASE_SERVER + \
                    ';DATABASE=' + DATABASE_NAME + \
                    ';Uid=' + DATABASE_USERNAME + \
                    ';Pwd=' + DATABASE_PASSWORD + \
                    ';Encrypt=yes' + \
                    ';TrustServerCertificate=no' + \
                    ';Connection Timeout=30;'

    def check_connection(self): 
        with pyodbc.connect(self.ODBC) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT @@version;")
                row = cursor.fetchone()
                while row:
                    print(row[0])
                    print("Successfully logged in!!")
                    row = cursor.fetchone()
                
    def insert_stock(self, item_name, number_of_item):
        try:
            with pyodbc.connect(self.ODBC) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"INSERT INTO Stock (ItemName, NumberOfItem) VALUES (?, ?);", (item_name, number_of_item))
                    print(f"Item '{item_name}' with quantity {number_of_item} inserted successfully.")
        except pyodbc.Error as e:
            if e.args[0] == '23000':
                with pyodbc.connect(self.ODBC) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(f"UPDATE Stock SET NumberOfItem = NumberOfItem + 1 WHERE ItemName = ?;", [item_name])
                        print(f"Item '{item_name}' quantity updated by 1.")
            else:
                print(f"An error occurred: {e}")

    def delete_stock(self, item_name):
        try:
            with pyodbc.connect(self.ODBC) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE FROM Stock WHERE ItemName = ?;", [item_name])
                    print(f"Item '{item_name}' deleted successfully.")
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")

    def insert_at_once(self, data_dict):
        try:
            recipt_items = data_dict['明細']
            
            for item in recipt_items:
                self.insert_stock(item['商品名'], item['数量'])
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")

    def get_all_items(self):
        '''
        在庫リストから商品をすべて取得する関数
        '''
        try:
            with pyodbc.connect(self.ODBC) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ItemName, NumberOfItem FROM Stock;")
                    rows = cursor.fetchall()
                    items = [{"item_name": row[0], "item_quantity": row[1]} for row in rows]
                    data = json.dumps(items, ensure_ascii=False)
                    return json.loads(data)
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return None
        
    def insert_to_deletedlist(self, item_name, number_of_item):
        '''
        在庫リストから削除されたものを家にないものリストに追加する関数

        引数
        - item_name: 在庫リストから削除されたもの
        '''
        try:
            with pyodbc.connect(self.ODBC) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"INSERT INTO Stock (ItemName, NumberOfItem) VALUES (?, ?);", (item_name, number_of_item))
                    print(f"Item '{item_name}' with quantity {number_of_item} inserted to DeletedStock successfully.")
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_deleted_items(self):
        '''
        家にないものをすべて取得する関数
        '''
        try:
            with pyodbc.connect(self.ODBC) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ItemName, NumberOfItem FROM DeletedStock;")
                    rows = cursor.fetchall()
                    items = [{"name": row[0], "quantity": row[1]} for row in rows]
                    data = json.dumps(items, ensure_ascii=False)
                    return json.loads(data)
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return None