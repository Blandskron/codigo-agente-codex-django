# Skill: Advanced Django ORM & SQL Retrieval

## Descripción
Capacidad para extraer, cruzar y transformar datos desde la base de datos utilizando herramientas avanzadas de Django.

## Estándares de Implementación Obligatorios

1. **Optimización de Relaciones (N+1):**
   - Utilizar SIEMPRE `select_related()` para relaciones de clave foránea (OneToOne, ForeignKey) cuando se necesiten datos del modelo relacionado.
   - Utilizar SIEMPRE `prefetch_related()` para relaciones inversas y ManyToMany.

2. **Filtrado Avanzado:**
   - Usar objetos `Q` (`from django.db.models import Q`) para condiciones complejas con operadores lógicos (OR `|`, AND `&`, NOT `~`).

3. **Operaciones a Nivel de Base de Datos:**
   - Usar expresiones `F` (`from django.db.models import F`) para comparaciones de campos dentro del mismo registro o actualizaciones atómicas.
   - Utilizar `annotate()` para añadir campos calculados por fila.
   - Utilizar `aggregate()` para resúmenes de todo el QuerySet (SUM, AVG, COUNT).

4. **Integración SQL (Cuando el ORM no es suficiente):**
   - Nivel 1: Usar `RawSQL` dentro de `annotate()` o `filter()`.
   - Nivel 2: Usar `Model.objects.raw()` para mapear consultas puras a instancias del modelo.
   - Nivel 3: Usar `connection.cursor()` únicamente para CTEs (Common Table Expressions) complejas o funciones analíticas específicas del motor DB.