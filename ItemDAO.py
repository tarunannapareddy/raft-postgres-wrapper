import psycopg2
from psycopg2 import Error
from DBConnector import *

class ItemDAO:
    def __init__(self):
        self.conn = DBConnector.get_product_connection()

    def add_item(self, item_id,category,seller_id,name,
                    quantity,sale_price,keywords,condition):
        try:
            with self.conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO item (item_id, category, seller_id, name, quantity, sale_price, keywords, condition)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    item_id,
                    category,
                    seller_id,
                    name,
                    quantity,
                    sale_price,
                    keywords,
                    condition
                ))
                self.conn.commit()
                return item_id
        except Error as e:
            print("Error while adding item:", e)
            return ""

    def update_item_price(self, item_id, new_sale_price):
        try:
            with self.conn.cursor() as cursor:
                update_query = "UPDATE item SET sale_price = %s WHERE item_id = %s"
                cursor.execute(update_query, (new_sale_price, item_id))
                self.conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print("Error while updating item price:", e)
            return False
    #
    def get_item(self, item_id):
        item=[]
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT * FROM item WHERE item_id = %s"
                cursor.execute(query, (item_id,))
                row = cursor.fetchone()
                if row:
                    return  {"item_id":row[0],
                    "category":row[1],
                    "seller_id":row[2],
                    "name":row[3],
                    "quantity":row[4],
                    "sale_price":row[5],
                    "keywords":row[6],
                    "condition":row[7]} # Assuming Item class constructor matches database columns order
                else:
                    return {}
        except Error as e:
            print("Error while getting item:", e)
            return {}
    #
    def get_items_by_seller_id(self, seller_id):
        items = []
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT * FROM item WHERE seller_id = %s"
                cursor.execute(query, (seller_id,))
                rows = cursor.fetchall()
                for row in rows:
                    items.append({"item_id":row[0],
                    "category":row[1],
                    "seller_id":row[2],
                    "name":row[3],
                    "quantity":row[4],
                    "sale_price":row[5],
                    "keywords":row[6],
                    "condition":row[7]})  # Assuming Item class constructor matches database columns order
        except Error as e:
            print("Error while getting items by seller ID:", e)
        return items
    #
    def update_item_quantity(self, item_id, quantity_to_reduce):
        try:
            with self.conn.cursor() as cursor:
                update_query = "UPDATE item SET quantity = quantity - %s WHERE item_id = %s"
                delete_query = "DELETE FROM item WHERE item_id = %s"

                cursor.execute(update_query, (quantity_to_reduce, item_id))
                if cursor.rowcount > 0:
                    self.conn.commit()
                    item = self.get_item(item_id)
                    if item and item["quantity"] == 0:
                        cursor.execute(delete_query, (item_id))
                        self.conn.commit()
                    return True
        except Error as e:
            print("Error while updating item quantity:", e)
        return False
    #
    def get_items_by_category_and_keywords(self, category_id, keywords_list):
        items = []
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT * FROM item WHERE category = %s AND keywords && %s"
                cursor.execute(query, (category_id, keywords_list))
                rows = cursor.fetchall()
                for row in rows:
                    items.append({"item_id":row[0],
                    "category":row[1],
                    "seller_id":row[2],
                    "name":row[3],
                    "quantity":row[4],
                    "sale_price":row[5],
                    "keywords":row[6],
                    "condition":row[7]})  # Assuming Item class constructor matches database columns order
        except Error as e:
            print("Error while getting items by category and keywords:", e)
        return items
