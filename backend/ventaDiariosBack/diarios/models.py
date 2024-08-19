from django.db import models

class DiarioVendido(models.Model):
    nombre = models.CharField(max_length=255)
    valor = models.IntegerField()

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    nombre = models.CharField(max_length=255)
    codigo_barras = models.CharField(max_length=255, unique=True)
    numero_identificador = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class Devolucion(models.Model):
    imagen = models.ImageField(upload_to='devoluciones/')
    fecha = models.DateField()

    def __str__(self):
        return f"Devolución {self.id} - {self.fecha}"
