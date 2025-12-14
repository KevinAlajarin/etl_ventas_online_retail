-- Inicializacion de miembros por defecto

SET IDENTITY_INSERT dw.DimCustomer ON;
INSERT INTO dw.DimCustomer (customer_key, customer_id_bk, customer_name)
VALUES (-1, -1, 'Unknown Customer');
SET IDENTITY_INSERT dw.DimCustomer OFF;

SET IDENTITY_INSERT dw.DimProduct ON;
INSERT INTO dw.DimProduct (product_key, stock_code_bk, description, category)
VALUES (-1, 'UNK', 'Unknown Product', 'Unknown');
SET IDENTITY_INSERT dw.DimProduct OFF;

SET IDENTITY_INSERT dw.DimCountry ON;
INSERT INTO dw.DimCountry (country_key, country_name)
VALUES (-1, 'Unknown Country');
SET IDENTITY_INSERT dw.DimCountry OFF;