-- Membuat tabel jika belum ada
CREATE TABLE IF NOT EXISTS robot_cleaners (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100),
    price NUMERIC(10, 2),
    battery_life INTEGER,
    weight REAL,
    cleaning_mode VARCHAR(50),
    warranty_years INTEGER,
    stock_availability VARCHAR(20),
    user_rating NUMERIC(3, 1),
    release_date DATE
);

ALTER TABLE robot_cleaners 
    ALTER COLUMN stock_availability TYPE VARCHAR(20);


-- Memasukkan data fake ke dalam tabel
INSERT INTO robot_cleaners (product_id, product_name, price, battery_life, weight, cleaning_mode, warranty_years, stock_availability, user_rating, release_date)
SELECT 
    'RB-' || lpad(g::TEXT, 4, '0') AS product_id,
    initcap(substring(md5(random()::text), 1, 8) || ' Cleaner') AS product_name,
    round(CAST(random() * 800 + 200 AS NUMERIC), 2) AS price,
    (random() * 9 + 1)::INTEGER AS battery_life,
    round(CAST(random() * 3 + 2 AS NUMERIC), 2) AS weight,
    (ARRAY['Dry', 'Wet', 'Hybrid'])[floor(random() * 3) + 1] AS cleaning_mode,
    (random() * 4 + 1)::INTEGER AS warranty_years,
    (ARRAY['In Stock', 'Out of Stock', 'Pre-Order'])[floor(random() * 3) + 1] AS stock_availability,
    round(CAST(random() * 2 + 3 AS NUMERIC), 1) AS user_rating,
    CURRENT_DATE - (random() * 365 * 5)::INTEGER AS release_date
FROM generate_series(1, 1000) g;
