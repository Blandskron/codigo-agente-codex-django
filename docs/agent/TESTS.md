# Testing Standards for ORM Queries

Todo código de recuperación de datos debe ser verificable. Al proponer una solución, el agente debe considerar estos estándares para las pruebas:

## Requisitos de Pruebas
1. **Aislamiento:** Las pruebas deben ejecutarse sobre una base de datos de test temporal (comportamiento por defecto de Django `TestCase`).
2. **Validación de Performance (Crítico):**
   - Toda consulta compleja debe incluir una aserción de cantidad de queries utilizando `self.assertNumQueries(n)`. Esto garantiza matemáticamente que no se introdujo un problema N+1.
3. **Preparación de Datos (Fixtures/Factories):**
   - Las pruebas deben incluir la creación explícita de los datos mínimos necesarios (`TestData`) usando `bulk_create` o factories para evaluar las funciones de filtrado.

## Formato de Salida
Las pruebas deben entregarse estructuradas para ubicarse en `tests/test_selectors.py` o `tests/test_managers.py`.