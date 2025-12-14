CREATE OR ALTER VIEW dw.vw_sales_by_country AS
SELECT 
    c.country_name,
    COUNT(DISTINCT fs.invoice_no) AS TotalOrders,
    SUM(fs.line_total) AS TotalRevenue,
    AVG(fs.line_total) AS AvgOrderValue,
    SUM(CASE WHEN fs.is_return = 1 THEN 1 ELSE 0 END) AS TotalReturns
FROM dw.FactSales fs
JOIN dw.DimCountry c ON fs.country_key = c.country_key
GROUP BY c.country_name;