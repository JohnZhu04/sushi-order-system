CREATE TABLE seats (
  seat_id INT NOT NULL,
  is_available BOOLEAN DEFAULT true,
  PRIMARY KEY (seat_id)
);

CREATE TABLE customers (
  customer_id CHAR(36) NOT NULL,
  seat_id INT,
  PRIMARY KEY (customer_id),
  FOREIGN KEY (seat_id) REFERENCES seats(seat_id)
);

CREATE TABLE categories (
  category_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (category_id)
);

CREATE TABLE sushis (
  sushi_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  has_wasabi BOOLEAN DEFAULT false,
  price DECIMAL(10, 2) NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (sushi_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE drinks (
  drink_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  PRIMARY KEY (drink_id)
);

CREATE TABLE orders (
  order_id INT NOT NULL,
  customer_id VARCHAR(10) NOT NULL,
  total_price DECIMAL(10, 2) NOT NULL,
  status INT NOT NULL,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_details (
  order_detail_id INT NOT NULL,
  order_id INT NOT NULL,
  item_type INT NOT NULL,
  item_id INT NOT NULL,
  topping INT,
  size INT,
  quantity INT NOT NULL,
  has_wasabi BOOLEAN DEFAULT false,
  price DECIMAL(10, 2) NOT NULL,
  status INT NOT NULL,
  ordered_at DATETIME NOT NULL,
  PRIMARY KEY (order_detail_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CHECK (item_type IN (0, 1)),
  CHECK (topping IS NULL OR item_type = 1),
  CHECK (size IS NULL OR item_type = 1)
);

CREATE TABLE stocks (
  stock_id INT NOT NULL AUTO_INCREMENT,
  item_type INT NOT NULL,
  item_id INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (stock_id),
  CHECK (item_type IN (0, 1))
);


-- insert sample data
INSERT INTO seats (seat_id) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
INSERT INTO categories (name) VALUES ('A'), ('B'), ('C');
INSERT INTO sushis (name, has_wasabi, price, category_id) VALUES ('Sushi 1', true, 100, 1), ('Sushi 2', false, 200, 2), ('Sushi 3', true, 300, 1), ('Sushi 4', false, 400, 3), ('Sushi 5', true, 500, 1);
INSERT INTO drinks (drink_id, name, price) VALUES (1, 'Drink 1', 100), (2, 'Drink 2', 200), (3, 'Drink 3', 300), (4, 'Drink 4', 400), (5, 'Drink 5', 500);
INSERT INTO stocks (stock_id, item_type, item_id, quantity) VALUES (1, 0, 1, 1), (2, 0, 2, 2), (3, 0, 3, 3), (4, 0, 4, 4), (5, 0, 5, 5), (6, 1, 1, 1), (7, 1, 2, 2), (8, 1, 3, 3), (9, 1, 4, 4), (10, 1, 5, 5);