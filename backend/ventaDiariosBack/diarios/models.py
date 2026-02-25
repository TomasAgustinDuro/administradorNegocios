from django.db import models
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio_venta = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=255, unique=True)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.precio_venta < 0:
            raise ValidationError("El valor no puede ser negativo.")
        if self.stock < 0:
            raise ValidationError("El valor no puede ser negativo.")
        if self.stock_minimo < 0:
            raise ValidationError("El valor no puede ser negativo.")


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    fecha = models.DateField()
    anulada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Venta {self.id} - {self.producto.nombre}"

    def clean(self):
        if self.precio_unitario < 0:
            raise ValidationError("El precio_unitario no puede ser negativo.")
        if self.total < 0:
            raise ValidationError("La total no puede ser negativo.")
        if self.cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        if not self.fecha:
            raise ValidationError("Debe proporcionar una fecha para la venta.")
        if self.cantidad > self.producto.stock:
            raise ValidationError("No hay suficiente stock")

    def save(self, *args, **kwargs):
        # Bloquear edición de ventas existentes
        if self.pk and not kwargs.pop("force_update", False):
            raise ValidationError(
                "No se puede modificar una venta. Créela nueva o anúlela."
            )

        # Solo descontar stock al crear
        if not self.pk:
            if self.cantidad > self.producto.stock:
                raise ValidationError("No hay suficiente stock")

            self.total = self.cantidad * self.precio_unitario
            self.producto.stock -= self.cantidad
            self.producto.save()

        super().save(*args, **kwargs)

    def anular(self):
        """Anular venta y devolver stock"""
        if self.anulada:
            raise ValidationError("La venta ya está anulada")

        self.anulada = True
        self.producto.stock += self.cantidad
        self.producto.save()
        self.save(force_update=True)


class Devolucion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha = models.DateField()
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return f"Devolución {self.id} - {self.fecha}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.producto.stock += self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)
