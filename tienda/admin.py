from django.contrib import admin

from .models import Categoria, DetalleVenta, Inventario, Producto, Venta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "es_activa")
    list_filter = ("es_activa",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "precio_base",
        "fecha_lanzamiento",
        "calificacion_metacritic",
    )
    list_filter = ("categoria",)
    search_fields = ("titulo",)
    list_select_related = ("categoria",)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "sucursal",
        "cantidad_disponible",
        "fecha_ultima_reposicion",
    )
    list_filter = ("sucursal",)
    search_fields = ("producto__titulo", "sucursal")
    list_select_related = ("producto",)


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    autocomplete_fields = ("producto",)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_transaccion", "metodo_pago", "total")
    list_filter = ("metodo_pago",)
    search_fields = ("=id",)
    inlines = (DetalleVentaInline,)


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_unitario")
    list_select_related = ("venta", "producto")
    autocomplete_fields = ("venta", "producto")
