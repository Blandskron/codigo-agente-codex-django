# Runbook: Flujo de Resolución de Consultas

Cuando el humano solicite resolver un problema de recuperación de datos, el agente debe seguir estrictamente esta secuencia:

1. **Fase de Ingesta:**
   - Identificar qué entidades del `DATA_SCHEMA.md` están involucradas.
   - Determinar si el resultado esperado es un `QuerySet` (instancias), un diccionario (`values()`), o un valor escalar (resultado de `aggregate`).

2. **Fase de Propuesta Lógica (Pre-código):**
   - Explicar brevemente en lenguaje natural cómo se estructurará la consulta (ej: "Primero filtraremos con Q, luego anotaremos la suma...").
   - Identificar posibles cuellos de botella de rendimiento.

3. **Fase de Implementación:**
   - Escribir el código aislando la lógica en métodos dentro de un Custom `Manager` o en funciones de capa de servicio/selectores.
   - Entregar el código completo, modular y listo para copiar y pegar.

4. **Fase de SQL Profiling (Simulada):**
   - Mostrar el equivalente aproximado en SQL que generará el ORM para demostrar que la consulta es eficiente.