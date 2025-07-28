-- First create missing base tables that should exist
CREATE TABLE IF NOT EXISTS emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    user_id INT,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email_address (email_address),
    INDEX idx_user_id (user_id)
);

CREATE TABLE IF NOT EXISTS service_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status ENUM('UP', 'DOWN', 'MAINTENANCE') DEFAULT 'UP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_service_name (service_name),
    INDEX idx_status (status)
);

-- Test schema alterations - add columns, modify constraints
-- Check if columns exist before adding them
SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = DATABASE() AND table_name = 'emails' AND column_name = 'email_verified') = 0, 
    'ALTER TABLE emails ADD COLUMN email_verified BOOLEAN DEFAULT FALSE, ADD COLUMN verification_token VARCHAR(255) NULL, ADD COLUMN verified_at TIMESTAMP NULL', 
    'SELECT "Columns already exist" as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add index for performance if it doesn't exist
SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS WHERE table_schema = DATABASE() AND table_name = 'emails' AND index_name = 'idx_emails_verified') = 0,
    'CREATE INDEX idx_emails_verified ON emails(email_verified)',
    'SELECT "Index already exists" as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Modify existing table structure - check if columns exist before adding
SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = DATABASE() AND table_name = 'service_status' AND column_name = 'health_score') = 0,
    'ALTER TABLE service_status ADD COLUMN health_score INT DEFAULT 100, ADD COLUMN last_check_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ADD COLUMN error_message TEXT NULL',
    'SELECT "Columns already exist" as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create a view for active services
DROP VIEW IF EXISTS active_services;
CREATE VIEW active_services AS
SELECT 
    id,
    service_name,
    status,
    health_score,
    updated_at,
    last_check_at,
    CASE 
        WHEN health_score >= 90 THEN 'Excellent'
        WHEN health_score >= 70 THEN 'Good'
        WHEN health_score >= 50 THEN 'Fair'
        ELSE 'Poor'
    END as health_rating
FROM service_status 
WHERE status = 'UP' AND health_score > 0;
