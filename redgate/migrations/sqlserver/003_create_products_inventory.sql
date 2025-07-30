-- Redgate SQL Server Migration: Create products and inventory system
-- Migration: 003_create_products_inventory
-- Description: Product catalog and inventory management
-- Author: Database Team
-- Date: 2025-07-30

-- Create categories table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[categories]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[categories] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(100) NOT NULL UNIQUE,
        [description] NVARCHAR(MAX),
        [parent_id] INT NULL,
        [is_active] BIT DEFAULT 1,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        
        FOREIGN KEY ([parent_id]) REFERENCES [dbo].[categories]([id])
    );
    
    PRINT 'Redgate: Created categories table successfully';
END;

-- Create products table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[products]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[products] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(255) NOT NULL,
        [description] NVARCHAR(MAX),
        [sku] NVARCHAR(50) NOT NULL UNIQUE,
        [category_id] INT,
        [price] DECIMAL(10,2) NOT NULL,
        [cost] DECIMAL(10,2),
        [weight] DECIMAL(8,2),
        [dimensions] NVARCHAR(100),
        [is_active] BIT DEFAULT 1,
        [created_at] DATETIME2 DEFAULT GETDATE(),
        [updated_at] DATETIME2 DEFAULT GETDATE(),
        
        FOREIGN KEY ([category_id]) REFERENCES [dbo].[categories]([id])
    );
    
    CREATE INDEX [idx_products_sku] ON [dbo].[products] ([sku]);
    CREATE INDEX [idx_products_category] ON [dbo].[products] ([category_id]);
    CREATE INDEX [idx_products_active] ON [dbo].[products] ([is_active]);
    
    PRINT 'Redgate: Created products table successfully';
END;

-- Create inventory table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[inventory]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[inventory] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [product_id] INT NOT NULL,
        [quantity_available] INT DEFAULT 0,
        [quantity_reserved] INT DEFAULT 0,
        [reorder_level] INT DEFAULT 0,
        [max_stock_level] INT,
        [location] NVARCHAR(100),
        [last_updated] DATETIME2 DEFAULT GETDATE(),
        
        FOREIGN KEY ([product_id]) REFERENCES [dbo].[products]([id]) ON DELETE CASCADE,
        UNIQUE([product_id], [location])
    );
    
    CREATE INDEX [idx_inventory_product] ON [dbo].[inventory] ([product_id]);
    CREATE INDEX [idx_inventory_low_stock] ON [dbo].[inventory] ([quantity_available]);
    
    PRINT 'Redgate: Created inventory table successfully';
END;
