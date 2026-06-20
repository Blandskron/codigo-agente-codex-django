from decimal import Decimal

from django.db.models import Count, DecimalField, IntegerField, QuerySet, Sum, Value
from django.db.models.functions import Coalesce

from .models import Categoria, Inventario, Producto, Venta


def obtener_resumen_dashboard() -> dict[str, int | Decimal]:
    """Retorna los indicadores generales del catálogo, inventario y ventas."""
    inventario = Inventario.objects.aggregate(
        unidades=Coalesce(Sum("cantidad_disponible"), 0)
    )
    ventas = Venta.objects.aggregate(
        cantidad=Count("id"),
        ingresos=Coalesce(
            Sum("total"),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=16, decimal_places=2),
        ),
    )
    return {
        "categorias": Categoria.objects.count(),
        "productos": Producto.objects.count(),
        "unidades_inventario": inventario["unidades"],
        "ventas": ventas["cantidad"],
        "ingresos": ventas["ingresos"],
    }


def obtener_productos_destacados(limite: int = 12) -> QuerySet[Producto]:
    """Retorna productos con su categoría y stock total sin consultas N+1."""
    return (
        Producto.objects.select_related("categoria")
        .annotate(
            stock_total=Coalesce(
                Sum("inventarios__cantidad_disponible"),
                0,
                output_field=IntegerField(),
            )
        )
        .order_by("-stock_total", "titulo")[:limite]
    )


def obtener_ventas_recientes(limite: int = 10) -> QuerySet[Venta]:
    """Retorna las ventas más recientes con líneas y unidades agregadas en SQL."""
    return (
        Venta.objects.annotate(
            cantidad_detalles=Count("detalles"),
            unidades=Coalesce(
                Sum("detalles__cantidad"),
                0,
                output_field=IntegerField(),
            ),
        )
        .order_by("-fecha_transaccion")[:limite]
    )


def obtener_inventario_por_sucursal() -> QuerySet[Inventario]:
    """Agrupa productos y unidades disponibles por sucursal."""
    return (
        Inventario.objects.values("sucursal")
        .annotate(
            productos=Count("producto", distinct=True),
            unidades=Sum("cantidad_disponible"),
        )
        .order_by("sucursal")
    )


def obtener_categorias_con_productos() -> QuerySet[Categoria]:
    """Retorna las categorías y el número de productos asociado a cada una."""
    return Categoria.objects.annotate(
        cantidad_productos=Count("productos")
    ).order_by("nombre")
