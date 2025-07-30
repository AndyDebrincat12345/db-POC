-- SQL Server Migration: Create monitoring and audit system
-- Migration: 004_create_monitoring_audit
-- Description: System monitoring and audit trails
-- Author: Database Team
-- Date: 2025-07-30

-- Create audit_log table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[audit_log]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[audit_log] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [table_name] NVARCHAR(100) NOT NULL,
        [record_id] INT,
        [action] NVARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
        [old_values] NVARCHAR(MAX), -- JSON format
        [new_values] NVARCHAR(MAX), -- JSON format
        [user_id] INT,
        [timestamp] DATETIME2 DEFAULT GETDATE(),
        [ip_address] NVARCHAR(45),
        [user_agent] NVARCHAR(MAX)
    );
    
    CREATE INDEX [idx_audit_table] ON [dbo].[audit_log] ([table_name]);
    CREATE INDEX [idx_audit_timestamp] ON [dbo].[audit_log] ([timestamp]);
    CREATE INDEX [idx_audit_user] ON [dbo].[audit_log] ([user_id]);
    
    PRINT 'Created audit_log table successfully';
END;

-- Create system_metrics table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[system_metrics]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[system_metrics] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [metric_name] NVARCHAR(100) NOT NULL,
        [metric_value] DECIMAL(15,4),
        [metric_unit] NVARCHAR(20),
        [recorded_at] DATETIME2 DEFAULT GETDATE(),
        [source] NVARCHAR(100)
    );
    
    CREATE INDEX [idx_metrics_name] ON [dbo].[system_metrics] ([metric_name]);
    CREATE INDEX [idx_metrics_timestamp] ON [dbo].[system_metrics] ([recorded_at]);
    
    PRINT 'Created system_metrics table successfully';
END;

-- Create a simple audit procedure for SQL Server
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_audit_table_changes]') AND type in (N'P', N'PC'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_audit_table_changes]
        @table_name NVARCHAR(100),
        @record_id INT,
        @action NVARCHAR(50),
        @user_id INT = NULL,
        @old_values NVARCHAR(MAX) = NULL,
        @new_values NVARCHAR(MAX) = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        INSERT INTO [dbo].[audit_log] (
            [table_name], 
            [record_id], 
            [action], 
            [user_id], 
            [old_values], 
            [new_values],
            [timestamp]
        )
        VALUES (
            @table_name, 
            @record_id, 
            @action, 
            @user_id, 
            @old_values, 
            @new_values,
            GETDATE()
        );
    END
    ');
    
    PRINT 'Created sp_audit_table_changes procedure successfully';
END;
