import psycopg2
from psycopg2 import Error
from DBConnector import *

class OrderDAO:
    def __init__(self):
        self.conn = DBConnector.get_product_connection()

    def create_order(self, buyer_id, status, transaction_id):
        try:
            with self.conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO customer_order (buyer_id, status, transaction_id)
                    VALUES (%s, %s, %s) RETURNING id
                """
                cursor.execute(insert_query, (buyer_id, status, transaction_id))
                self.conn.commit()
                return cursor.fetchone()[0]
        except Error as e:
            print("Error while creating order:", e)
            return False

    def update_order(self, status, transaction_id):
        try:
            with self.conn.cursor() as cursor:
                update_query = "UPDATE customer_order SET status = %s WHERE transaction_id = %s RETURNING id"
                cursor.execute(update_query, (status, transaction_id))
                self.conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print("Error while updating order:", e)
            return False

    def update_order_item(self, order_id, quantity, item_id):
        try:
            with self.conn.cursor() as cursor:
                insert_query = "INSERT INTO order_item (order_id, quantity, item_id) VALUES (%s, %s, %s) RETURNING id"
                cursor.execute(insert_query, (order_id, quantity, item_id))
                self.conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print("Error while updating order item:", e)
            return False
