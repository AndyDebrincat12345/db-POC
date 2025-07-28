-- Redgate Migration: Create comprehensive users table
-- This tests traditional SQL script approach

CREATE TABLE IF NOT EXISTS users_redgate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    salary DECIMAL(10,2),
    bio TEXT,
    preferences JSON,
    avatar_url VARCHAR(500),
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes separately for better readability and control
-- Note: UNIQUE constraints automatically create indexes, so username and email already have indexes
CREATE INDEX idx_users_redgate_last_login ON users_redgate(last_login_at);
CREATE INDEX idx_users_redgate_active_users ON users_redgate(is_active, created_at);

-- Add some sample data to test data handling
INSERT IGNORE INTO users_redgate (username, email, password_hash, first_name, last_name, is_active) VALUES
('admin', 'admin@example.com', 'hashed_password_1', 'System', 'Administrator', TRUE),
('testuser1', 'test1@example.com', 'hashed_password_2', 'Test', 'User One', TRUE),
('testuser2', 'test2@example.com', 'hashed_password_3', 'Test', 'User Two', FALSE);
