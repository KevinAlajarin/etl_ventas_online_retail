CREATE TABLE dw.FactSales (
    fact_sales_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    date_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    country_key INT NOT NULL,
    invoice_no VARCHAR(50) NOT NULL, -- Degenerate Dimension
    quantity INT,
    unit_price DECIMAL(18, 4),
    line_total DECIMAL(18, 4),
    is_return BIT,
    loaded_at DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Fact_Date FOREIGN KEY (date_key) REFERENCES dw.DimDate(date_key),
    CONSTRAINT FK_Fact_Product FOREIGN KEY (product_key) REFERENCES dw.DimProduct(product_key),
    CONSTRAINT FK_Fact_Customer FOREIGN KEY (customer_key) REFERENCES dw.DimCustomer(customer_key),
    CONSTRAINT FK_Fact_Country FOREIGN KEY (country_key) REFERENCES dw.DimCountry(country_key)
);

CREATE INDEX IDX_FactSales_InvoiceDate ON dw.FactSales(date_key);