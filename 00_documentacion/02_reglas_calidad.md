# Reglas de Calidad de Datos

Estas reglas se aplican estrictamente en la capa de transformación (Python - `clean_staging.py`) antes de cargar al DW.

| ID | Regla | Descripción | Acción |
|----|-------|-------------|--------|
| DQ_01 | **Eliminación de Cancelaciones** | Si `InvoiceNo` comienza con 'C' | **Eliminar registro**. |
| DQ_02 | **Precios Inválidos** | Si `UnitPrice` <= 0 | **Eliminar registro** (No hay venta real). |
| DQ_03 | **Cantidades Negativas** | Si `Quantity` < 0 (y no es 'C', aunque 'C' ya se borró) | Marcar flag `is_return = TRUE`. Mantener registro si representa ajuste de inventario/retorno sin cancelación explícita. |
| DQ_04 | **Cliente Desconocido** | Si `CustomerID` es NULL o Vacío | Asignar Business Key `-1`. En Dimensión se mapea a 'Unknown Customer'. |
| DQ_05 | **Descripciones Vacías** | Si `Description` es NULL | Imputar con string 'No Description'. |
| DQ_06 | **Duplicados Exactos** | Filas idénticas en CSV | **Deduplicar** manteniendo la primera ocurrencia. |