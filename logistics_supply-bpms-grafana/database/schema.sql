-- Create schema for logistics database
CREATE SCHEMA IF NOT EXISTS logistics;

-- Dimension tables
CREATE TABLE IF NOT EXISTS dim_product (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    unit_weight DECIMAL(10, 2),
    unit_volume DECIMAL(10, 2),
    unit_cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id SERIAL PRIMARY KEY,
    location_code VARCHAR(50) UNIQUE NOT NULL,
    location_name VARCHAR(255) NOT NULL,
    location_type VARCHAR(50), -- warehouse, customer, supplier
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(20),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_vehicle (
    vehicle_id SERIAL PRIMARY KEY,
    vehicle_code VARCHAR(50) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50),
    capacity_weight DECIMAL(10, 2),
    capacity_volume DECIMAL(10, 2),
    fuel_type VARCHAR(50),
    maintenance_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_type VARCHAR(50),
    contact_person VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_time (
    date_id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    week INT,
    day INT,
    day_of_week INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Fact tables
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    origin_location_id INT REFERENCES dim_location(location_id),
    destination_location_id INT REFERENCES dim_location(location_id),
    order_date_id INT REFERENCES dim_time(date_id),
    delivery_date_id INT REFERENCES dim_time(date_id),
    quantity INT,
    weight DECIMAL(10, 2),
    volume DECIMAL(10, 2),
    order_value DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES dim_product(product_id),
    location_id INT REFERENCES dim_location(location_id),
    date_id INT REFERENCES dim_time(date_id),
    quantity INT,
    unit_cost DECIMAL(10, 2),
    total_value DECIMAL(10, 2),
    min_stock_level INT,
    max_stock_level INT,
    reorder_point INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_transportation (
    shipment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES fact_orders(order_id),
    vehicle_id INT REFERENCES dim_vehicle(vehicle_id),
    departure_location_id INT REFERENCES dim_location(location_id),
    arrival_location_id INT REFERENCES dim_location(location_id),
    departure_date_id INT REFERENCES dim_time(date_id),
    arrival_date_id INT REFERENCES dim_time(date_id),
    distance DECIMAL(10, 2),
    fuel_consumption DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_route_optimization (
    route_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES dim_vehicle(vehicle_id),
    date_id INT REFERENCES dim_time(date_id),
    total_distance DECIMAL(10, 2),
    total_cost DECIMAL(10, 2),
    total_stops INT,
    total_weight DECIMAL(10, 2),
    total_volume DECIMAL(10, 2),
    route_sequence JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_orders_customer ON fact_orders(customer_id);
CREATE INDEX idx_orders_product ON fact_orders(product_id);
CREATE INDEX idx_orders_dates ON fact_orders(order_date_id, delivery_date_id);
CREATE INDEX idx_inventory_product_location ON fact_inventory(product_id, location_id);
CREATE INDEX idx_transportation_order ON fact_transportation(order_id);
CREATE INDEX idx_transportation_vehicle ON fact_transportation(vehicle_id);
CREATE INDEX idx_transportation_dates ON fact_transportation(departure_date_id, arrival_date_id);
CREATE INDEX idx_route_optimization_vehicle ON fact_route_optimization(vehicle_id);
CREATE INDEX idx_route_optimization_date ON fact_route_optimization(date_id);

-- Functions
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers
CREATE TRIGGER update_dim_product_updated_at
    BEFORE UPDATE ON dim_product
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dim_location_updated_at
    BEFORE UPDATE ON dim_location
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dim_vehicle_updated_at
    BEFORE UPDATE ON dim_vehicle
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dim_customer_updated_at
    BEFORE UPDATE ON dim_customer
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fact_orders_updated_at
    BEFORE UPDATE ON fact_orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fact_inventory_updated_at
    BEFORE UPDATE ON fact_inventory
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fact_transportation_updated_at
    BEFORE UPDATE ON fact_transportation
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fact_route_optimization_updated_at
    BEFORE UPDATE ON fact_route_optimization
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 