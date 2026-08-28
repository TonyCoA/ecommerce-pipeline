import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_products_above_price(minimum_price):
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT product_id, title, price
                FROM products
                WHERE price >= %s
                ORDER BY price DESC;
                """,
                (minimum_price,),
            )

            products = cursor.fetchall()

        return products

    finally:
        connection.close()


products = get_products_above_price(5000)

for product in products:
    print(product)