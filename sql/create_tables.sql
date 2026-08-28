DROP TABLE IF EXISTS product_images;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    price NUMERIC(10,2) CHECK (price >= 0),
    discount_percentage NUMERIC(5,2) CHECK (discount_percentage >= 0),
    rating NUMERIC(3,2) CHECK (rating >= 0 AND rating <= 5),
    stock INTEGER CHECK (stock >= 0),
    brand TEXT,
    sku TEXT UNIQUE,
    weight NUMERIC,
    width NUMERIC,
    height NUMERIC,
    depth NUMERIC,
    warranty_information TEXT,
    shipping_information TEXT,
    availability_status TEXT,
    return_policy TEXT,
    minimum_order_quantity INTEGER CHECK (minimum_order_quantity >= 0),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    barcode TEXT,
    qr_code_url TEXT,
    thumbnail_url TEXT
);

CREATE TABLE reviews (
    review_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date TIMESTAMP,
    reviewer_name TEXT,
    reviewer_email TEXT,

    CONSTRAINT fk_reviews_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

CREATE TABLE product_images (
    image_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,

    CONSTRAINT fk_product_images_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);