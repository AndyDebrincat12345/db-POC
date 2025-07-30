-- SQL Server Migration: Create roles and permissions system
-- Migration: 002_create_roles_permissions
-- Description: RBAC system with roles and permissions
-- Author: Database Team
-- Date: 2025-07-30

-- Create roles table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[roles]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[roles] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(50) NOT NULL UNIQUE,
        [description] NVARCHAR(MAX),
        [is_active] BIT DEFAULT 1,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        [updated_at] DATETIME2 DEFAULT GETDATE()
    );
    
    PRINT 'Created roles table successfully';
END;

-- Create permissions table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[permissions]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[permissions] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(50) NOT NULL UNIQUE,
        [description] NVARCHAR(MAX),
        [resource] NVARCHAR(100),
        [action] NVARCHAR(50),
        [created_at] DATETIME2 DEFAULT GETDATE()
    );
    
    PRINT 'Created permissions table successfully';
END;

-- Create role_permissions junction table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[role_permissions]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[role_permissions] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [role_id] INT NOT NULL,
        [permission_id] INT NOT NULL,
        [granted_at] DATETIME2 DEFAULT GETDATE(),
        
        FOREIGN KEY ([role_id]) REFERENCES [dbo].[roles]([id]) ON DELETE CASCADE,
        FOREIGN KEY ([permission_id]) REFERENCES [dbo].[permissions]([id]) ON DELETE CASCADE,
        
        UNIQUE([role_id], [permission_id])
    );
    
    PRINT 'Created role_permissions table successfully';
END;

-- Create user_roles junction table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user_roles]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[user_roles] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [user_id] INT NOT NULL,
        [role_id] INT NOT NULL,
        [assigned_at] DATETIME2 DEFAULT GETDATE(),
        [assigned_by] INT,
        
        FOREIGN KEY ([user_id]) REFERENCES [dbo].[users_comprehensive]([id]) ON DELETE CASCADE,
        FOREIGN KEY ([role_id]) REFERENCES [dbo].[roles]([id]) ON DELETE CASCADE,
        
        UNIQUE([user_id], [role_id])
    );
    
    PRINT 'Created user_roles table successfully';
END;
