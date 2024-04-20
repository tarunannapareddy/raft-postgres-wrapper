import psycopg2
from psycopg2 import Error
from DBConnector import *

class CartDAO:
    def __init__(self):
        self.conn = DBConnector.get_product_connection()

    def get_cart(self, buyer_id):
        query = "SELECT * FROM cart WHERE buyer_id = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (buyer_id,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # returning the cart ID
                else:
                    return self.create_cart(buyer_id)
        except Error as e:
            print("Error while getting cart:", e)
        return -1

    def create_cart(self, buyer_id):
        query = "INSERT INTO cart (buyer_id) VALUES (%s) RETURNING id"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (buyer_id,))
                self.conn.commit()
                return cursor.fetchone()[0]
        except Error as e:
            print("Error while creating cart:", e)
        return -1

    def update_cart_quantity(self, cart_id, item_id, quantity_change):
        update_query = "UPDATE cart_item SET quantity = quantity + %s WHERE cart_id = %s AND item_id = %s"
        insert_query = "INSERT INTO cart_item (cart_id, item_id, quantity) VALUES (%s, %s, %s)"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(update_query, (quantity_change, cart_id, item_id))
                if cursor.rowcount > 0:
                    self.conn.commit()
                    return True
                elif quantity_change > 0:
                    cursor.execute(insert_query, (cart_id, item_id, quantity_change))
                    self.conn.commit()
                    return cursor.rowcount > 0
        except Error as e:
            print("Error while updating cart quantity:", e)
        return False

    def delete_cart(self, cart_id):
        query = "DELETE FROM cart_item WHERE cart_id = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (cart_id,))
                self.conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print("Error while deleting cart:", e)
        return False

    def get_cart_items(self, cart_id):
        query = "SELECT * FROM cart_item WHERE cart_id = %s"
        cart_items = []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (cart_id,))
                for row in cursor.fetchall():
                    cart_items.append({
                        "id": row[0],
                        "cart_id": row[1],
                        "item_id": row[2],
                        "quantity": row[3]
                    })
        except Error as e:
            print("Error while getting cart items:", e)
        return cart_items
