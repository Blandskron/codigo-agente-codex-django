from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    es_activa = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )
    titulo = models.CharField(max_length=200)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_lanzamiento = models.DateField()
    calificacion_metacritic = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.titulo


class Inventario(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="inventarios",
    )
    sucursal = models.CharField(max_length=100)
    cantidad_disponible = models.IntegerField()
    fecha_ultima_reposicion = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.producto} - {self.sucursal}"


class Venta(models.Model):
    fecha_transaccion = models.DateTimeField()
    metodo_pago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"Venta #{self.pk}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_venta",
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.cantidad} x {self.producto}"

