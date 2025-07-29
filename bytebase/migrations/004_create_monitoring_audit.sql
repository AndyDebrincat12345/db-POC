-- Bytebase Migration: Create monitoring and audit features
-- Migration: 004_create_monitoring_audit
-- Description: System monitoring and audit logging capabilities
-- Author: Database Team
-- Date: 2025-07-29

-- Create service status monitoring table
CREATE TABLE IF NOT EXISTS service_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    health_score INT DEFAULT 100,
    last_check_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create low stock products view
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

-- Create audit logging procedure
DELIMITER $$
CREATE PROCEDURE log_audit_event(
    IN p_table_name VARCHAR(100),
    IN p_operation_type VARCHAR(10),
    IN p_record_id VARCHAR(50),
    IN p_old_values JSON,
    IN p_new_values JSON,
    IN p_changed_by INT,
    IN p_ip_address VARCHAR(45)
)
BEGIN
    INSERT INTO audit_log (
        table_name, operation_type, record_id, 
        old_values, new_values, changed_by, ip_address
    ) VALUES (
        p_table_name, p_operation_type, p_record_id,
        p_old_values, p_new_values, p_changed_by, p_ip_address
    );
END$$
DELIMITER ;
