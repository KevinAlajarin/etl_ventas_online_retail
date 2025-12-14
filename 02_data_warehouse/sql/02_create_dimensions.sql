-- DimCountry
CREATE TABLE dw.DimCountry (
    country_key INT IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);

-- DimCustomer
CREATE TABLE dw.DimCustomer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id_bk BIGINT NOT NULL, -- Business Key
    customer_name VARCHAR(100) DEFAULT 'Unknown',
    effective_date DATETIME DEFAULT GETDATE()
);
CREATE INDEX IDX_DimCustomer_BK ON dw.DimCustomer(customer_id_bk);

-- DimProduct
CREATE TABLE dw.DimProduct (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    stock_code_bk VARCHAR(50) NOT NULL, -- Business Key
    description VARCHAR(255),
    category VARCHAR(100), -- Inferida o manual
    last_updated DATETIME DEFAULT GETDATE()
);
CREATE INDEX IDX_DimProduct_BK ON dw.DimProduct(stock_code_bk);

-- DimDate (Estándar)
CREATE TABLE dw.DimDate (
    date_key INT PRIMARY KEY, -- Formato YYYYMMDD
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    month_num INT,
    month_name VARCHAR(20),
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BIT
);