import psycopg2
from psycopg2 import Error

class DBConnector:
    customer_db_url = "dbname=customer user=postgres password=admin host=localhost port=5432"
    product_db_url = "dbname=product user=postgres password=admin host=localhost port=5432"

    @staticmethod
    def get_customer_connection():
        try:
            connection = psycopg2.connect(DBConnector.customer_db_url)
            return connection
        except Error as e:
            print("Failed creating customer DB connection:", e)

    @staticmethod
    def get_product_connection():
        try:
            connection = psycopg2.connect(DBConnector.product_db_url)
            return connection
        except Error as e:
            print("Failed creating product DB connection:", e)