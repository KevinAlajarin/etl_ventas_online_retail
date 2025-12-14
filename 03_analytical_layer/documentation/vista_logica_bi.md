# Vista Logica para Business Intelligence

Este documento mapea las necesidades del Dashboard de Power BI con las vistas SQL creadas en la capa analítica.

## 1. Estrategia de Conexion
Para maximizar el rendimiento y la mantenibilidad, Power BI no debe conectarse directamente a las tablas crudas del DW (`dw.FactSales`), sino a estas vistas preparadas que encapsulan lógica de negocio.

## 2. Mapeo de Vistas

### A. Vista: `dw.vw_sales_daily`
* **Proposito:** Análisis temporal de alto nivel.
* **Uso en Dashboard:**
    * Gráfico de tendencia mensual (Página 1).
    * Comparativas YoY (Year over Year).
    * Slicers de fecha.

### B. Vista: `dw.vw_sales_by_product`
* **Proposito:** Rendimiento de inventario y catalogo.
* **Uso en Dashboard:**
    * Tabla "Top 10 Productos" (Página 1).
    * Matriz de Categorías (Página 2).
    * Identificacion de "Slow movers" (productos sin venta).

### C. Vista: `dw.vw_sales_by_country`
* **Proposito:** Análisis geográfico.
* **Uso en Dashboard:**
    * Mapa o Grafico de Barras por País (Página 1).
    * Análisis de mercados emergentes.

### D. Vista: `dw.vw_customer_orders`
* **Proposito:** Segmentacion de clientes (RFM simplificado).
* **Uso en Dashboard:**
    * Histograma de frecuencia de compra.
    * Identificacion de clientes VIP (Página 3).
    * Calculo de Churn rate (basado en `last_purchase_date`).

### E. Vista: `dw.vw_kpis`
* **Proposito:** Tarjetas de alto nivel.
* **Uso en Dashboard:**
    * KPI Cards: Revenue, AOV, Orders (Todas las páginas).