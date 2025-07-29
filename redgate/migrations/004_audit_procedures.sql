-- Redgate Migration: Audit and stored procedures
-- Script: 004_audit_procedures.sql
-- Description: Audit logging system and stored procedures
-- Execution: Manual review and deployment via Redgate
-- Date: 2025-07-29

-- Audit logging procedure
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
    -- Note: This procedure assumes audit_log table exists
    -- In Redgate workflow, this would be created via schema comparison
    INSERT INTO audit_log (
        table_name, operation_type, record_id, 
        old_values, new_values, changed_by, ip_address
    ) VALUES (
        p_table_name, p_operation_type, p_record_id,
        p_old_values, p_new_values, p_changed_by, p_ip_address
    );
END$$
DELIMITER ;

-- Sample data insertion for testing
INSERT INTO locations (name, address) VALUES 
('Main Warehouse', '123 Industrial Blvd, City, State'),
('Secondary Storage', '456 Storage Ave, City, State');

-- Performance monitoring setup
-- Note: In real Redgate deployment, this would include
-- performance baseline capture and monitoring scripts
