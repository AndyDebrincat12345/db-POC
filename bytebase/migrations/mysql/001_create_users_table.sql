-- Bytebase Migration: Create comprehensive users table
-- Migration: 001_create_users_table
-- Description: Initial user management system with comprehensive fields
-- Author: Database Team
-- Date: 2025-07-29

CREATE TABLE IF NOT EXISTS users_comprehensive (
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_last_login (last_login_at),
    INDEX idx_active_users (is_active, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
