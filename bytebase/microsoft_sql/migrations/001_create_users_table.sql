-- SQL Server Migration: Create comprehensive users table
-- Migration: 001_create_users_table
-- Description: Initial user management system with comprehensive fields
-- Author: Database Team
-- Date: 2025-07-30

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users_comprehensive]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[users_comprehensive] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [username] NVARCHAR(50) NOT NULL UNIQUE,
        [email] NVARCHAR(255) NOT NULL UNIQUE,
        [password_hash] NVARCHAR(255) NOT NULL,
        [first_name] NVARCHAR(100),
        [last_name] NVARCHAR(100),
        [date_of_birth] DATE,
        [phone_number] NVARCHAR(20),
        [is_active] BIT DEFAULT 1,
        [salary] DECIMAL(10,2),
        [bio] NVARCHAR(MAX),
        [preferences] NVARCHAR(MAX), -- JSON storage
        [avatar_url] NVARCHAR(500),
        [last_login_at] DATETIME2 NULL,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        [updated_at] DATETIME2 DEFAULT GETDATE()
    );
    
    -- Indexes for performance
    CREATE INDEX [idx_username] ON [dbo].[users_comprehensive] ([username]);
    CREATE INDEX [idx_email] ON [dbo].[users_comprehensive] ([email]);
    CREATE INDEX [idx_last_login] ON [dbo].[users_comprehensive] ([last_login_at]);
    CREATE INDEX [idx_active_users] ON [dbo].[users_comprehensive] ([is_active], [created_at]);
    
    PRINT 'Created users_comprehensive table successfully';
END
ELSE
BEGIN
    PRINT 'Table users_comprehensive already exists';
END;
