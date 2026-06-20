# Juega Siempre — Django Advanced ORM

Aplicación Django para la gestión de inventario y ventas de **Juega Siempre**, una tienda especializada en videojuegos, consolas y accesorios. El proyecto sirve como base para implementar y medir consultas complejas con el ORM de Django y PostgreSQL, incluyendo filtrados, agregaciones, funciones de ventana y estrategias para evitar consultas N+1.

## Tecnologías

- Python 3.12+
- Django 5.2
- PostgreSQL
- Faker para generar datos de demostración
- Bootstrap 5 para el esqueleto del dashboard

## Requisitos previos

- Python 3.12 o superior disponible en `PATH`.
- PostgreSQL en ejecución en `localhost:5432`.
- Una base de datos llamada `tienda_codex_db`.
- Un usuario PostgreSQL con permisos sobre esa base de datos.

La configuración de desarrollo incluida utiliza estos valores:

| Parámetro | Valor |
|---|---|
| Base de datos | `tienda_codex_db` |
| Usuario | `postgres` |
| Contraseña | `admin1234` |
| Host | `localhost` |
| Puerto PostgreSQL | `5432` |

> Las credenciales incluidas son sólo para desarrollo local. En un despliegue real deben trasladarse a variables de entorno y mantenerse fuera del control de versiones.

## Instalación local

1. Clona el repositorio y entra a su directorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd codigo-agente-codex-django
   ```

2. Crea y activa un entorno virtual:

   En Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   En Linux o macOS:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Revisa la conexión PostgreSQL en `config/settings.py` y adapta las credenciales si tu entorno local utiliza valores diferentes.

## Migraciones

Aplica el esquema de Django y las tablas de la tienda:

```bash
python manage.py migrate
```

Para confirmar el estado de las migraciones:

```bash
python manage.py showmigrations
```

## Carga masiva de datos

El comando `envio_masivo` elimina los datos existentes de las tablas de negocio y genera un conjunto reproducible con categorías, productos, inventarios, ventas y detalles de venta:

```bash
python manage.py envio_masivo
```

La carga predeterminada crea 10 categorías, 100 productos, inventario para cada producto en dos o tres sucursales y 500 ventas con entre uno y cinco detalles. Todos los registros se escriben por lotes dentro de una transacción atómica.

Para obtener otro conjunto reproducible, indica una semilla distinta:

```bash
python manage.py envio_masivo --semilla 12345
```

## Servidor de desarrollo

Inicia Django en el puerto establecido por el proyecto:

```bash
python manage.py runserver 8080
```

Abre [http://127.0.0.1:8080/](http://127.0.0.1:8080/) para acceder al dashboard o [http://127.0.0.1:8080/admin/](http://127.0.0.1:8080/admin/) para acceder a la administración de Django.

## Estructura principal

```text
config/                       Configuración global y rutas raíz
tienda/                       Modelos, administración, vistas y lógica de negocio
tienda/management/commands/   Comandos personalizados de Django
templates/tienda/             Plantillas del dashboard
docs/agent/                   Esquema, seguridad y normas del agente
```

## Verificaciones útiles

```bash
python manage.py check
python manage.py migrate --check
```
