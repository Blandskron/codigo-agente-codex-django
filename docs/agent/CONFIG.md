# Environment & Context Configuration

## Entorno Tecnológico
- **Framework:** Django (Asumir versión 4.2+ para soporte de características ORM modernas).
- **Database Engine:** PostgreSQL (Asumir este motor para permitir el uso de funciones avanzadas como `ArrayAgg`, `StringAgg`, y Window Functions si fuera necesario).
- **Patrón Arquitectónico:** "Fat Models, Skinny Views" adaptado. La lógica de recuperación compleja debe residir en `QuerySets` personalizados encadenables o en un archivo `selectors.py` separado, NUNCA dentro de las vistas (`views.py` o `api.py`).

## Convenciones de Código
- Uso de `Type Hints` obligatorios en métodos de selección (ej: `-> QuerySet[Producto]:`).
- Nombres de variables descriptivos en español (alineado al dominio).
- Documentación interna de funciones usando Docstrings estándar detallando qué retorna la consulta.

## Despliegue Local y Ejecución
- **Puerto de desarrollo:** El servidor local SIEMPRE debe iniciarse en el puerto `8080` (ej: `python manage.py runserver 8080`), a menos que se indique lo contrario en el prompt.
- **Gestión de dependencias:** Asegúrate de mantener un archivo `requirements.txt` actualizado con cada instalación que realices.