CREATE OR ALTER VIEW dw.vw_sales_daily AS
SELECT 
    d.full_date,
    d.year,
    d.month_name,
    COUNT(DISTINCT fs.invoice_no) as total_orders,
    SUM(fs.quantity) as total_quantity,
    SUM(fs.line_total) as total_revenue,
    AVG(fs.line_total) as avg_line_value
FROM dw.FactSales fs
JOIN dw.DimDate d ON fs.date_key = d.date_key
WHERE fs.is_return = 0 
GROUP BY d.full_date, d.year, d.month_name;