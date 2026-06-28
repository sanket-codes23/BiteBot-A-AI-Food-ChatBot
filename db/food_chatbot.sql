

-- =====================================================
-- TABLE: categories
-- =====================================================

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================================
-- TABLE: food_items
-- =====================================================

CREATE TABLE food_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(100) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_category
    FOREIGN KEY(category_id)
    REFERENCES categories(category_id)
);

-- =====================================================
-- TABLE: orders
-- =====================================================

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2) DEFAULT 0
);

-- =====================================================
-- TABLE: order_items
-- =====================================================

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    item_id INT NOT NULL,

    quantity INT NOT NULL,

    subtotal DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
    ON DELETE CASCADE,

    CONSTRAINT fk_food
    FOREIGN KEY(item_id)
    REFERENCES food_items(item_id)
);

-- =====================================================
-- TABLE: order_tracking
-- =====================================================

CREATE TABLE order_tracking (
    order_id INT PRIMARY KEY,

    status VARCHAR(50) NOT NULL,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tracking
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
    ON DELETE CASCADE
);



-- =====================================================
-- INSERT CATEGORIES
-- =====================================================

INSERT INTO categories(category_name) VALUES
('Indian'),
('Fast Food'),
('Desserts'),
('Beverages');



-- =====================================================
-- INSERT FOOD ITEMS
-- =====================================================

INSERT INTO food_items(food_name,category_id,price) VALUES

('Paneer Butter Masala',1,280),
('Shahi Paneer',1,260),
('Dal Makhani',1,220),
('Veg Biryani',1,240),
('Butter Naan',1,40),
('Tandoori Roti',1,20),

('Pizza',2,350),
('Burger',2,180),
('French Fries',2,120),
('Pasta',2,220),
('Sandwich',2,150),
('Momos',2,140),

('Gulab Jamun',3,80),
('Rasmalai',3,100),
('Chocolate Brownie',3,120),
('Vanilla Ice Cream',3,90),

('Cold Coffee',4,140),
('Lassi',4,90),
('Coke',4,50),
('Pepsi',4,50),
('Mineral Water',4,20),
('Orange Juice',4,110);



-- =====================================================
-- SAMPLE ORDER
-- =====================================================

INSERT INTO orders(customer_name,total_price)
VALUES
('Demo Customer',630);



-- =====================================================
-- SAMPLE ORDER ITEMS
-- =====================================================

INSERT INTO order_items(order_id,item_id,quantity,subtotal)
VALUES
(1,7,1,350),
(1,8,1,180),
(1,19,2,100);



-- =====================================================
-- SAMPLE TRACKING
-- =====================================================

INSERT INTO order_tracking(order_id,status)
VALUES
(1,'Preparing');