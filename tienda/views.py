from django.shortcuts import render

from .selectors import (
    obtener_categorias_con_productos,
    obtener_inventario_por_sucursal,
    obtener_productos_destacados,
    obtener_resumen_dashboard,
    obtener_ventas_recientes,
)


def inicio(request):
    """Renderiza el dashboard con datos agregados de la tienda."""
    contexto = {
        "resumen": obtener_resumen_dashboard(),
        "productos": obtener_productos_destacados(),
        "ventas_recientes": obtener_ventas_recientes(),
        "inventario_sucursales": obtener_inventario_por_sucursal(),
        "categorias": obtener_categorias_con_productos(),
    }
    return render(request, "tienda/inicio.html", contexto)
