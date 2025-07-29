-- Redgate Migration: Inventory management system
-- Script: 003_inventory_system.sql
-- Description: Complete inventory tracking and management
-- Execution: Deployment package via Redgate SQL Source Control
-- Date: 2025-07-29

-- Inventory tracking table
CREATE TABLE IF NOT EXISTS inventory_lq (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    location_id INT NOT NULL,
    quantity INT DEFAULT 0,
    reserved_quantity INT DEFAULT 0,
    last_count_at TIMESTAMP NULL,
    last_movement_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY fk_inventory_product (product_id) 
        REFERENCES products(id),
    FOREIGN KEY fk_inventory_location (location_id) 
        REFERENCES locations(id),
        
    INDEX idx_product_location (product_id, location_id),
    INDEX idx_last_movement (last_movement_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Low stock monitoring view
CREATE VIEW low_stock_products AS
SELECT 
    p.id,
    p.name,
    p.sku,
    SUM(i.quantity) as total_quantity,
    p.low_stock_threshold,
    CASE 
        WHEN SUM(i.quantity) <= p.low_stock_threshold THEN 'CRITICAL'
        WHEN SUM(i.quantity) <= p.low_stock_threshold * 1.5 THEN 'LOW'
        ELSE 'OK'
    END as stock_status
FROM products p
LEFT JOIN inventory_lq i ON p.id = i.product_id
WHERE p.is_active = TRUE
GROUP BY p.id, p.name, p.sku, p.low_stock_threshold
HAVING SUM(i.quantity) <= p.low_stock_threshold * 2;
