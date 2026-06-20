# Domain Model & Data Schema

El proyecto modela la gestión de inventario y ventas de una tienda de videojuegos. El agente debe usar este esquema lógico para diseñar sus consultas ORM.

## Entidades Principales

1. **Categoria:**
   - `id` (PK)
   - `nombre` (Ej: RPG, Shooter, Consola, Accesorio)
   - `es_activa` (Boolean)

2. **Producto (Videojuegos y Hardware):**
   - `id` (PK)
   - `categoria_id` (FK -> Categoria)
   - `titulo` (String)
   - `precio_base` (Decimal)
   - `fecha_lanzamiento` (Date)
   - `calificacion_metacritic` (Integer, nullable)

3. **Inventario:**
   - `id` (PK)
   - `producto_id` (FK -> Producto)
   - `sucursal` (String)
   - `cantidad_disponible` (Integer)
   - `fecha_ultima_reposicion` (DateTime)

4. **Venta:**
   - `id` (PK)
   - `fecha_transaccion` (DateTime)
   - `metodo_pago` (String)
   - `total` (Decimal)

5. **DetalleVenta:**
   - `id` (PK)
   - `venta_id` (FK -> Venta)
   - `producto_id` (FK -> Producto)
   - `cantidad` (Integer)
   - `precio_unitario` (Decimal)