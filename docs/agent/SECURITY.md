# Security Guardrails: SQL Injection Prevention

La seguridad es primordial, especialmente al combinar el ORM con sentencias SQL crudas para resolver las consultas más complejas del proyecto.

## Reglas de Parametrización
1. **NUNCA usar f-strings o concatenación (`+`)** para insertar variables dinámicas dentro de una consulta SQL cruda (`RawSQL`, `.raw()`, o cursores).
2. **SIEMPRE usar parámetros de paso:**
   - Para `.raw()`: `Producto.objects.raw('SELECT * FROM app_producto WHERE categoria_id = %s', [id_categoria])`
   - Para cursores: `cursor.execute("SELECT ... WHERE nombre = %s", [nombre])`
3. **Validación de Input:** Aunque se asume que las vistas validan los datos, la capa de acceso a datos (selectores/managers) debe asegurar el tipado correcto antes de ejecutar `Q()` objects complejos basados en input externo.