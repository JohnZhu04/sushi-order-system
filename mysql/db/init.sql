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
  stock_id INT NOT NULL,
  item_type INT NOT NULL,
  item_id INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (stock_id),
  FOREIGN KEY (item_type) REFERENCES categories(category_id),
  CHECK (item_type IN (0, 1))
);