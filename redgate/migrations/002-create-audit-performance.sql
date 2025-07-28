-- Redgate Migration: Create audit and logging system
-- This tests complex scenarios like triggers and partitioning

CREATE TABLE IF NOT EXISTS audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    record_id VARCHAR(50) NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_by INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_table_operation (table_name, operation_type),
    INDEX idx_changed_by (changed_by),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (changed_by) REFERENCES users_redgate(id) ON DELETE SET NULL
);

-- Create a procedure for audit logging
DELIMITER //
DROP PROCEDURE IF EXISTS log_audit_event//
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
END //
DELIMITER ;

-- Create performance test table with large dataset capability
CREATE TABLE IF NOT EXISTS performance_test (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    price DECIMAL(10,2),
    quantity INT DEFAULT 0,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
    tags JSON,
    metadata JSON,
    created_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category_status (category_id, status),
    INDEX idx_price (price),
    INDEX idx_created_date (created_date),
    INDEX idx_name (name)
);
