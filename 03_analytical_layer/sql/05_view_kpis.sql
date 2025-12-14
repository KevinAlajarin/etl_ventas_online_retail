CREATE OR ALTER VIEW dw.vw_kpis AS
SELECT 
    d.year,
    d.month_num,
    SUM(fs.line_total) as Revenue,
    COUNT(DISTINCT fs.invoice_no) as Orders,
    SUM(fs.line_total) / NULLIF(COUNT(DISTINCT fs.invoice_no), 0) as AOV, -- Average Order Value
    COUNT(DISTINCT fs.customer_key) as DistinctCustomers
FROM dw.FactSales fs
JOIN dw.DimDate d ON fs.date_key = d.date_key
WHERE fs.is_return = 0
GROUP BY d.year, d.month_num;