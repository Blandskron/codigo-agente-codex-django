# Agent Permissions & Boundaries

## Permisos Concedidos
- **Lectura de Código:** Acceso total a leer modelos, vistas, managers y serializers.
- **Creación de Código:** Autorizado para crear custom `Managers` y `QuerySets` en archivos separados (ej: `managers.py`, `selectors.py`).
- **Análisis de DB:** Autorizado para solicitar y analizar los planes de ejecución (`EXPLAIN`) de las consultas generadas.

## Permisos de Ejecución (Terminal)
- **Autorizado:** Tienes permiso total para ejecutar comandos bash/shell en este entorno local.
- **Autorizado:** Ejecutar inicialización de proyectos (`django-admin startproject`, `python manage.py startapp`).
- **Autorizado:** Instalar dependencias necesarias mediante `pip` (ej. `psycopg2-binary`, `django`).
- **Autorizado:** Ejecutar migraciones de base de datos de forma autónoma (`makemigrations`, `migrate`).
- **Autorizado:** Iniciar el servidor de desarrollo en puertos específicos.

## Restricciones Estrictas (Denegado)
- **NO modificar el Schema destructivamente:** El agente no debe alterar la estructura de las tablas (`models.py`) sin autorización explícita. La tarea es *recuperación*, no diseño de base de datos.
- **NO sobreescribir métodos nativos destructivos:** Prohibido modificar métodos `delete()` o `save()` de los modelos en esta fase.
- **NO instalar dependencias externas no estándar:** Limitarse al ORM nativo de Django. Si se requiere una librería de terceros (ej: `django-cte`), debe ser solicitada al humano.