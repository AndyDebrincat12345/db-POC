-- Test file: Auto-detection verification
-- Script: 005_test_auto_detection.sql
-- Description: Verify that GUI automatically picks up new migration files

-- Simple test table creation
CREATE TABLE IF NOT EXISTS test_auto_detection (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_message VARCHAR(100) DEFAULT 'Auto-detection works!',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert test data
INSERT INTO test_auto_detection (test_message) VALUES 
('File 005 was automatically detected by GUI');
