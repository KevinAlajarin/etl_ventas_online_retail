IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'staging')
BEGIN
    EXEC('CREATE SCHEMA [staging]')
END
GO

IF OBJECT_ID('staging.raw_retail', 'U') IS NOT NULL DROP TABLE staging.raw_retail;
CREATE TABLE staging.raw_retail (
    InvoiceNo VARCHAR(50),
    StockCode VARCHAR(50),
    Description VARCHAR(255),
    Quantity VARCHAR(50),
    InvoiceDate VARCHAR(50),
    UnitPrice VARCHAR(50),
    CustomerID VARCHAR(50),
    Country VARCHAR(100)
);

IF OBJECT_ID('staging.clean_retail', 'U') IS NOT NULL DROP TABLE staging.clean_retail;
CREATE TABLE staging.clean_retail (
    InvoiceNo VARCHAR(50),
    StockCode VARCHAR(50),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(18, 4),
    CustomerID BIGINT, 
    Country VARCHAR(100),
    LineTotal DECIMAL(18, 4),
    IsReturn BIT
);