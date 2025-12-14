# Diseño del Dashboard Retail (Power BI)

## Modelo de Datos en PBI
* Importar vistas de `dw.vw_*` o importar tablas Dimensiones y Fact directamente.
* Relaciones: Star Schema estándar (1:* de Dims a Fact).

## Pagina 1: Executive Overview
* **KPIs (Tarjetas):** Total Revenue (CY), Total Orders, AOV, % Returns.
* **Grafico Principal:** Línea de tendencia mensual Revenue vs LY (Last Year - usar DAX `CALCULATE(SUM(Revenue), SAMEPERIODLASTYEAR(...))`).
* **Tabla:** Top 10 Productos por Revenue.
* **Pie:** Revenue por País (Top 5 + Otros).

## Pagina 2: Product Performance
* **Matrix:** Categoría -> Producto. Métricas: Quantity Sold, Revenue, Returns.
* **Scatter Plot:** Precio Unitario vs Cantidad Vendida (Elasticidad básica).

## Pagina 3: Customer Insights
* **Histograma:** Distribución de Clientes por número de órdenes (1, 2-5, 5-10, 10+).
* **Tabla:** Top Clientes por Revenue (Pareto analysis).