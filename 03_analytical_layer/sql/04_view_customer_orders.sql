CREATE OR ALTER VIEW dw.vw_customer_orders AS
SELECT 
    c.customer_id_bk AS CustomerID,
    MAX(d.full_date) AS LastPurchaseDate,
    DATEDIFF(day, MAX(d.full_date), GETDATE()) AS DaysSinceLastPurchase,
    COUNT(DISTINCT fs.invoice_no) AS TotalOrders,
    SUM(fs.line_total) AS TotalLifetimeValue,
    AVG(fs.line_total) AS AvgTicketSize
FROM dw.FactSales fs
JOIN dw.DimCustomer c ON fs.customer_key = c.customer_key
JOIN dw.DimDate d ON fs.date_key = d.date_key
WHERE c.customer_id_bk <> -1 
GROUP BY c.customer_id_bk;