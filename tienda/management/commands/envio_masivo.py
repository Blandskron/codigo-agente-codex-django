import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from tienda.models import Categoria, DetalleVenta, Inventario, Producto, Venta


CANTIDAD_PRODUCTOS = 100
CANTIDAD_VENTAS = 500
TAMANO_LOTE = 500

CATEGORIAS = (
    "RPG",
    "Shooter",
    "Aventura",
    "Estrategia",
    "Deportes",
    "Carreras",
    "Consolas",
    "Accesorios",
    "Realidad Virtual",
    "Coleccionables",
)

SUCURSALES = ("Santiago Centro", "Providencia", "Viña del Mar")
METODOS_PAGO = ("Débito", "Crédito", "Efectivo", "Transferencia")

TITULOS_POR_CATEGORIA = {
    "RPG": ("Crónicas de", "Legado de", "Reinos de"),
    "Shooter": ("Operación", "Comando", "Zona de combate"),
    "Aventura": ("El misterio de", "Viaje a", "Secretos de"),
    "Estrategia": ("Imperios de", "Conquista de", "Fronteras de"),
    "Deportes": ("Liga", "Campeones", "Estadio"),
    "Carreras": ("Velocidad", "Circuito", "Rally"),
    "Consolas": ("Consola Nova", "Consola Pixel", "Consola Quantum"),
    "Accesorios": ("Control Pro", "Teclado Gamer", "Audífonos Élite"),
    "Realidad Virtual": ("Visor VR", "Aventura VR", "Kit Inmersivo"),
    "Coleccionables": ("Figura de", "Edición de colección", "Estatua de"),
}

COMPLEMENTOS = (
    "Aether",
    "Andes",
    "Arcadia",
    "Aurora",
    "Centinela",
    "Dragón",
    "Eclipse",
    "Fénix",
    "Galaxia",
    "Horizonte",
    "Nébula",
    "Titán",
)


class Command(BaseCommand):
    help = "Reemplaza los datos de la tienda por un conjunto masivo y realista."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--semilla",
            type=int,
            default=20260619,
            help="Semilla aleatoria para reproducir exactamente el conjunto de datos.",
        )

    def handle(self, *args, **options) -> None:
        semilla = options["semilla"]
        random.seed(semilla)
        Faker.seed(semilla)
        generador = Faker("es_CL")

        with transaction.atomic():
            self._limpiar_datos()
            categorias = self._crear_categorias()
            productos = self._crear_productos(categorias, generador)
            inventarios = self._crear_inventarios(productos, generador)
            ventas, detalles = self._crear_ventas(productos, generador)

        self.stdout.write(self.style.SUCCESS("Carga masiva completada correctamente."))
        self.stdout.write(f"Categorías: {len(categorias)}")
        self.stdout.write(f"Productos: {len(productos)}")
        self.stdout.write(f"Inventarios: {len(inventarios)}")
        self.stdout.write(f"Ventas: {len(ventas)}")
        self.stdout.write(f"Detalles de venta: {len(detalles)}")

    def _limpiar_datos(self) -> None:
        """Elimina datos de negocio en el orden requerido por sus claves foráneas."""
        DetalleVenta.objects.all().delete()
        Venta.objects.all().delete()
        Inventario.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()

    def _crear_categorias(self) -> list[Categoria]:
        """Crea el catálogo base de categorías mediante una inserción por lote."""
        categorias = [
            Categoria(nombre=nombre, es_activa=True) for nombre in CATEGORIAS
        ]
        return Categoria.objects.bulk_create(categorias, batch_size=TAMANO_LOTE)

    def _crear_productos(
        self,
        categorias: list[Categoria],
        generador: Faker,
    ) -> list[Producto]:
        """Genera cien productos coherentes, repartidos entre las categorías."""
        productos: list[Producto] = []

        for indice in range(CANTIDAD_PRODUCTOS):
            categoria = categorias[indice % len(categorias)]
            prefijos = TITULOS_POR_CATEGORIA[categoria.nombre]
            titulo = (
                f"{prefijos[(indice // len(categorias)) % len(prefijos)]} "
                f"{COMPLEMENTOS[indice % len(COMPLEMENTOS)]} {indice + 1:03d}"
            )
            es_software = categoria.nombre in {
                "RPG",
                "Shooter",
                "Aventura",
                "Estrategia",
                "Deportes",
                "Carreras",
            }
            precio_minimo, precio_maximo = (
                (Decimal("14990"), Decimal("69990"))
                if es_software
                else (Decimal("19990"), Decimal("699990"))
            )
            precio = Decimal(
                random.randrange(int(precio_minimo), int(precio_maximo) + 1, 1000)
            )
            fecha_lanzamiento = generador.date_between(
                start_date="-8y",
                end_date="today",
            )

            productos.append(
                Producto(
                    categoria=categoria,
                    titulo=titulo,
                    precio_base=precio,
                    fecha_lanzamiento=fecha_lanzamiento,
                    calificacion_metacritic=random.randint(55, 98)
                    if es_software
                    else None,
                )
            )

        return Producto.objects.bulk_create(productos, batch_size=TAMANO_LOTE)

    def _crear_inventarios(
        self,
        productos: list[Producto],
        generador: Faker,
    ) -> list[Inventario]:
        """Distribuye cada producto en dos o tres sucursales sin duplicarlas."""
        inventarios: list[Inventario] = []
        zona_horaria = timezone.get_current_timezone()

        for producto in productos:
            for sucursal in random.sample(SUCURSALES, random.choice((2, 3))):
                inventarios.append(
                    Inventario(
                        producto=producto,
                        sucursal=sucursal,
                        cantidad_disponible=random.randint(0, 80),
                        fecha_ultima_reposicion=generador.date_time_between(
                            start_date="-180d",
                            end_date="now",
                            tzinfo=zona_horaria,
                        ),
                    )
                )

        return Inventario.objects.bulk_create(
            inventarios,
            batch_size=TAMANO_LOTE,
        )

    def _crear_ventas(
        self,
        productos: list[Producto],
        generador: Faker,
    ) -> tuple[list[Venta], list[DetalleVenta]]:
        """Crea ventas del último año y calcula sus totales desde los detalles."""
        zona_horaria = timezone.get_current_timezone()
        ventas = [
            Venta(
                fecha_transaccion=generador.date_time_between(
                    start_date="-1y",
                    end_date="now",
                    tzinfo=zona_horaria,
                ),
                metodo_pago=random.choice(METODOS_PAGO),
                total=Decimal("0.00"),
            )
            for _ in range(CANTIDAD_VENTAS)
        ]
        ventas = Venta.objects.bulk_create(ventas, batch_size=TAMANO_LOTE)

        detalles: list[DetalleVenta] = []
        for venta in ventas:
            total_venta = Decimal("0.00")
            productos_vendidos = random.sample(productos, random.randint(1, 5))
            for producto in productos_vendidos:
                cantidad = random.randint(1, 3)
                factor_precio = random.choice(
                    (Decimal("0.85"), Decimal("0.90"), Decimal("1.00"))
                )
                precio_unitario = (producto.precio_base * factor_precio).quantize(
                    Decimal("0.01")
                )
                detalles.append(
                    DetalleVenta(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                    )
                )
                total_venta += precio_unitario * cantidad
            venta.total = total_venta.quantize(Decimal("0.01"))

        DetalleVenta.objects.bulk_create(detalles, batch_size=TAMANO_LOTE)
        Venta.objects.bulk_update(
            ventas,
            fields=("total",),
            batch_size=TAMANO_LOTE,
        )
        return ventas, detalles
