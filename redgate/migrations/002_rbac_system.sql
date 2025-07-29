-- Redgate Migration: Role-based access control
-- Script: 002_rbac_system.sql
-- Description: Add comprehensive role and permission management
-- Execution: Schema comparison and deployment via Redgate
-- Date: 2025-07-29

-- Roles table
CREATE TABLE IF NOT EXISTS roles_lq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Permissions table
CREATE TABLE IF NOT EXISTS permissions_lq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_resource_action (resource, action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Role-permissions junction table
CREATE TABLE IF NOT EXISTS role_permissions_lq (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INT NULL,
    
    PRIMARY KEY (role_id, permission_id),
    
    FOREIGN KEY fk_role_permissions_role (role_id) 
        REFERENCES roles_lq(id) ON DELETE CASCADE,
    FOREIGN KEY fk_role_permissions_permission (permission_id) 
        REFERENCES permissions_lq(id) ON DELETE CASCADE,
    FOREIGN KEY fk_role_permissions_granted_by (granted_by) 
        REFERENCES users_comprehensive(id) ON DELETE SET NULL,
        
    INDEX idx_role_permissions_permission (permission_id),
    INDEX idx_role_permissions_granted_by (granted_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
