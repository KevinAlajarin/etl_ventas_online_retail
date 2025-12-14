CREATE OR ALTER PROCEDURE dw.sp_load_fact_incremental
AS
BEGIN
    SET NOCOUNT ON;
    
    -- 1. Actualizar Dimensiones basado en Staging
    
    -- DimCountry
    INSERT INTO dw.DimCountry (country_name)
    SELECT DISTINCT Country 
    FROM staging.clean_retail s
    WHERE NOT EXISTS (SELECT 1 FROM dw.DimCountry d WHERE d.country_name = s.Country);

    -- DimCustomer (Solo IDs nuevos)
    INSERT INTO dw.DimCustomer (customer_id_bk, customer_name)
    SELECT DISTINCT CustomerID, 'Registered Customer'
    FROM staging.clean_retail s
    WHERE NOT EXISTS (SELECT 1 FROM dw.DimCustomer d WHERE d.customer_id_bk = s.CustomerID);

    -- DimProduct (Actualiza descripcion si cambia, inserta si es nuevo)
    MERGE dw.DimProduct AS target
    USING (SELECT DISTINCT StockCode, Description FROM staging.clean_retail) AS source
    ON (target.stock_code_bk = source.StockCode)
    WHEN MATCHED AND target.description <> source.Description THEN
        UPDATE SET description = source.Description, last_updated = GETDATE()
    WHEN NOT MATCHED THEN
        INSERT (stock_code_bk, description, category)
        VALUES (source.StockCode, source.Description, 'Uncategorized');

    -- 2. Obtener High Watermark (Ultima fecha cargada)
    DECLARE @LastLoadDate DATETIME;
    SELECT @LastLoadDate = ISNULL(MAX(last_load_date), '1900-01-01') FROM etl.control_table WHERE process_name = 'FactSales';

    -- 3. Cargar FactSales
    INSERT INTO dw.FactSales (
        date_key, product_key, customer_key, country_key, 
        invoice_no, quantity, unit_price, line_total, is_return
    )
    SELECT 
        CAST(CONVERT(VARCHAR(8), s.InvoiceDate, 112) AS INT) as date_key,
        p.product_key,
        c.customer_key,
        co.country_key,
        s.InvoiceNo,
        s.Quantity,
        s.UnitPrice,
        s.LineTotal,
        s.IsReturn
    FROM staging.clean_retail s
    INNER JOIN dw.DimProduct p ON s.StockCode = p.stock_code_bk
    INNER JOIN dw.DimCustomer c ON s.CustomerID = c.customer_id_bk
    INNER JOIN dw.DimCountry co ON s.Country = co.country_name
    WHERE s.InvoiceDate > @LastLoadDate;

    -- 4. Actualizar Control
    DECLARE @NewMaxDate DATETIME;
    SELECT @NewMaxDate = MAX(InvoiceDate) FROM staging.clean_retail;
    
    IF @NewMaxDate IS NOT NULL
    BEGIN
        UPDATE etl.control_table 
        SET last_load_date = @NewMaxDate, updated_at = GETDATE()
        WHERE process_name = 'FactSales';
    END
END
GO