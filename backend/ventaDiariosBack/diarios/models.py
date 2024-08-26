from django.db import models
from django.core.exceptions import ValidationError

class DiarioVendido(models.Model):
    nombre = models.CharField(max_length=255)
    valor = models.IntegerField()

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.valor < 0:
            raise ValidationError("El valor no puede ser negativo.")

class Inventario(models.Model):
    nombre = models.CharField(max_length=255)
    codigo_barras = models.CharField(max_length=255, unique=True)
    stock = models.IntegerField(default=0)
    vendido = models.IntegerField(default=0)
    restante = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.vendido < 0:
            raise ValidationError("La cantidad vendida no puede ser negativa.")
        if self.vendido > self.stock:
            raise ValidationError("La cantidad vendida no puede ser mayor al stock disponible.")

class Devolucion(models.Model):
    imagen = models.ImageField(upload_to='devoluciones/')
    fecha = models.DateField()

    def __str__(self):
        return f"Devolución {self.id} - {self.fecha}"

    def clean(self):
        if not self.imagen:
            raise ValidationError("Debe proporcionar una imagen para la devolución.")
        if not self.fecha:
            raise ValidationError("Debe proporcionar una fecha para la devolución.")
