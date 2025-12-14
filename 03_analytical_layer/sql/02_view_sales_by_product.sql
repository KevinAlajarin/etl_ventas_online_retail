CREATE OR ALTER VIEW dw.vw_sales_by_product AS
SELECT 
    p.stock_code_bk AS StockCode,
    p.description AS ProductName,
    p.category AS Category,
    SUM(fs.quantity) AS TotalQuantitySold,
    SUM(fs.line_total) AS TotalRevenue,
    COUNT(DISTINCT fs.invoice_no) AS TimesOrdered,
    DENSE_RANK() OVER (ORDER BY SUM(fs.line_total) DESC) as SalesRank
FROM dw.FactSales fs
JOIN dw.DimProduct p ON fs.product_key = p.product_key
WHERE fs.is_return = 0
GROUP BY p.stock_code_bk, p.description, p.category;