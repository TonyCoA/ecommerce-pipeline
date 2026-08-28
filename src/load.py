import json
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def load_products_json():
    """Read products from the raw JSON file."""
    with open("data/raw/products.json", "r", encoding="utf-8") as file:
        return json.load(file)


def validate_source(products):
    """Validate source data before loading it into PostgreSQL."""
    product_ids = [product["id"] for product in products]

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Duplicate product IDs found in source JSON.")

    for product in products:
        if product["price"] < 0:
            raise ValueError(
                f"Negative price found for product {product['id']}."
            )

        if product["stock"] < 0:
            raise ValueError(
                f"Negative stock found for product {product['id']}."
            )


def get_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def clear_child_tables(connection):
    """Clear reviews and images before reloading them."""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM reviews;")
        cursor.execute("DELETE FROM product_images;")


def upsert_products(connection, products):
    """Insert new products or update existing products."""
    with connection.cursor() as cursor:
        for product in products:
            cursor.execute(
                """
                INSERT INTO products (
                    product_id,
                    title,
                    description,
                    category,
                    price,
                    discount_percentage,
                    rating,
                    stock,
                    brand,
                    sku,
                    weight,
                    width,
                    height,
                    depth,
                    warranty_information,
                    shipping_information,
                    availability_status,
                    return_policy,
                    minimum_order_quantity,
                    created_at,
                    updated_at,
                    barcode,
                    qr_code_url,
                    thumbnail_url
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (product_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    category = EXCLUDED.category,
                    price = EXCLUDED.price,
                    discount_percentage = EXCLUDED.discount_percentage,
                    rating = EXCLUDED.rating,
                    stock = EXCLUDED.stock,
                    brand = EXCLUDED.brand,
                    sku = EXCLUDED.sku,
                    weight = EXCLUDED.weight,
                    width = EXCLUDED.width,
                    height = EXCLUDED.height,
                    depth = EXCLUDED.depth,
                    warranty_information = EXCLUDED.warranty_information,
                    shipping_information = EXCLUDED.shipping_information,
                    availability_status = EXCLUDED.availability_status,
                    return_policy = EXCLUDED.return_policy,
                    minimum_order_quantity = EXCLUDED.minimum_order_quantity,
                    created_at = EXCLUDED.created_at,
                    updated_at = EXCLUDED.updated_at,
                    barcode = EXCLUDED.barcode,
                    qr_code_url = EXCLUDED.qr_code_url,
                    thumbnail_url = EXCLUDED.thumbnail_url;
                """,
                (
                    product["id"],
                    product["title"],
                    product["description"],
                    product["category"],
                    product["price"],
                    product["discountPercentage"],
                    product["rating"],
                    product["stock"],
                    product.get("brand"),
                    product["sku"],
                    product["weight"],
                    product["dimensions"]["width"],
                    product["dimensions"]["height"],
                    product["dimensions"]["depth"],
                    product["warrantyInformation"],
                    product["shippingInformation"],
                    product["availabilityStatus"],
                    product["returnPolicy"],
                    product["minimumOrderQuantity"],
                    product["meta"]["createdAt"],
                    product["meta"]["updatedAt"],
                    product["meta"]["barcode"],
                    product["meta"]["qrCode"],
                    product["thumbnail"],
                ),
            )


def load_reviews(connection, products):
    """Load product reviews."""
    with connection.cursor() as cursor:
        for product in products:
            for review in product.get("reviews", []):
                cursor.execute(
                    """
                    INSERT INTO reviews (
                        product_id,
                        rating,
                        comment,
                        review_date,
                        reviewer_name,
                        reviewer_email
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        product["id"],
                        review["rating"],
                        review["comment"],
                        review["date"],
                        review["reviewerName"],
                        review["reviewerEmail"],
                    ),
                )


def load_images(connection, products):
    """Load product image URLs."""
    with connection.cursor() as cursor:
        for product in products:
            for image_url in product.get("images", []):
                cursor.execute(
                    """
                    INSERT INTO product_images (
                        product_id,
                        image_url
                    )
                    VALUES (%s, %s);
                    """,
                    (
                        product["id"],
                        image_url,
                    ),
                )


def validate_database(connection, products):
    """Validate loaded database data before committing."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM products;")
        database_product_count = cursor.fetchone()[0]

        if database_product_count != len(products):
            raise ValueError(
                "Product count mismatch: "
                f"source={len(products)}, "
                f"database={database_product_count}"
            )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reviews r
            LEFT JOIN products p
                ON r.product_id = p.product_id
            WHERE p.product_id IS NULL;
            """
        )
        orphan_reviews = cursor.fetchone()[0]

        if orphan_reviews > 0:
            raise ValueError(
                f"Found {orphan_reviews} orphan reviews."
            )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM product_images i
            LEFT JOIN products p
                ON i.product_id = p.product_id
            WHERE p.product_id IS NULL;
            """
        )
        orphan_images = cursor.fetchone()[0]

        if orphan_images > 0:
            raise ValueError(
                f"Found {orphan_images} orphan product images."
            )


def main():
    products = load_products_json()

    validate_source(products)

    connection = get_connection()

    try:
        clear_child_tables(connection)
        upsert_products(connection, products)
        load_reviews(connection, products)
        load_images(connection, products)
        validate_database(connection, products)

        connection.commit()

        print(f"Processed {len(products)} products successfully.")

    except Exception as error:
        connection.rollback()

        print("Load failed.")
        print(f"Error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()