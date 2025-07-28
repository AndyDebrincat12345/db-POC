-- Data seeding for comprehensive testing
-- Insert sample categories
INSERT IGNORE INTO categories (name, slug, description, parent_id, sort_order, is_active) VALUES
('Electronics', 'electronics', 'Electronic devices and gadgets', NULL, 1, TRUE),
('Computers', 'computers', 'Desktop and laptop computers', 1, 1, TRUE),
('Smartphones', 'smartphones', 'Mobile phones and accessories', 1, 2, TRUE),
('Home & Garden', 'home-garden', 'Home improvement and garden supplies', NULL, 2, TRUE),
('Furniture', 'furniture', 'Home and office furniture', 4, 1, TRUE);

-- Insert sample products with various data types
INSERT IGNORE INTO products (name, slug, description, sku, price, cost_price, weight, dimensions, category_id, brand, is_featured, stock_quantity, low_stock_threshold) VALUES
('MacBook Pro 16"', 'macbook-pro-16', 'High-performance laptop for professionals', 'MBP-16-2024', 2499.99, 1800.00, 2.1, '{"length": 35.79, "width": 24.59, "height": 1.68}', 2, 'Apple', TRUE, 25, 5),
('iPhone 15 Pro', 'iphone-15-pro', 'Latest iPhone with advanced camera system', 'IP15P-128', 999.99, 700.00, 0.187, '{"length": 14.67, "width": 7.09, "height": 0.83}', 3, 'Apple', TRUE, 100, 20),
('Samsung Galaxy S24', 'samsung-galaxy-s24', 'Android flagship with AI features', 'SGS24-256', 899.99, 650.00, 0.196, '{"length": 14.7, "width": 7.06, "height": 0.76}', 3, 'Samsung', TRUE, 75, 15),
('Gaming Chair Pro', 'gaming-chair-pro', 'Ergonomic chair for extended gaming sessions', 'GCP-BLK-001', 299.99, 150.00, 18.5, '{"length": 70, "width": 70, "height": 130}', 5, 'GameMax', FALSE, 40, 10);

-- Insert sample product variants
INSERT IGNORE INTO product_variants (product_id, name, sku, price, stock_quantity, attributes) VALUES
(1, 'MacBook Pro 16" Space Gray', 'MBP-16-SG', 2499.99, 15, '{"color": "Space Gray", "storage": "512GB", "memory": "16GB"}'),
(1, 'MacBook Pro 16" Silver', 'MBP-16-SL', 2499.99, 10, '{"color": "Silver", "storage": "512GB", "memory": "16GB"}'),
(2, 'iPhone 15 Pro Blue Titanium', 'IP15P-128-BT', 999.99, 50, '{"color": "Blue Titanium", "storage": "128GB"}'),
(2, 'iPhone 15 Pro Natural Titanium', 'IP15P-128-NT', 999.99, 50, '{"color": "Natural Titanium", "storage": "128GB"}');

-- Insert sample users with various scenarios
INSERT IGNORE INTO users (username, email, password_hash, first_name, last_name, date_of_birth, is_active, salary, preferences) VALUES
('john_admin', 'john@company.com', 'hashed_password_admin', 'John', 'Administrator', '1985-03-15', TRUE, 75000.00, '{"theme": "dark", "notifications": true, "language": "en"}'),
('sarah_manager', 'sarah@company.com', 'hashed_password_manager', 'Sarah', 'Manager', '1990-07-22', TRUE, 65000.00, '{"theme": "light", "notifications": true, "language": "en"}'),
('mike_user', 'mike@company.com', 'hashed_password_user', 'Mike', 'User', '1992-11-08', TRUE, 45000.00, '{"theme": "auto", "notifications": false, "language": "en"}'),
('inactive_user', 'inactive@company.com', 'hashed_password_inactive', 'Inactive', 'User', '1988-01-01', FALSE, NULL, '{}');

-- Insert sample roles and permissions
INSERT IGNORE INTO roles (name, description, is_system_role) VALUES
('admin', 'System administrator with full access', TRUE),
('manager', 'Department manager with limited admin access', FALSE),
('user', 'Regular user with basic access', FALSE),
('viewer', 'Read-only access to most resources', FALSE);

INSERT IGNORE INTO permissions (name, resource, action, description) VALUES
('users.create', 'users', 'create', 'Create new users'),
('users.read', 'users', 'read', 'View user information'),
('users.update', 'users', 'update', 'Update user information'),
('users.delete', 'users', 'delete', 'Delete users'),
('products.create', 'products', 'create', 'Create new products'),
('products.read', 'products', 'read', 'View product information'),
('products.update', 'products', 'update', 'Update product information'),
('products.delete', 'products', 'delete', 'Delete products');
