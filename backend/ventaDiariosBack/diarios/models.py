from django.db import models
from django.core.exceptions import ValidationError


class DiarioVendido(models.Model):
    """Representa un diario o revista registrado como venta del día.

    Attributes:
        nombre: Nombre del diario o revista vendido.
        valor: Precio de venta en pesos. No puede ser negativo.
    """

    nombre = models.CharField(max_length=255)
    valor = models.IntegerField()

    def __str__(self) -> str:
        """Retorna la representación legible del diario vendido."""
        return self.nombre

    def clean(self) -> None:
        """Valida que el valor de venta no sea negativo.

        Raises:
            ValidationError: Si el valor es menor a cero.
        """
        if self.valor < 0:
            raise ValidationError("El valor no puede ser negativo.")


class Inventario(models.Model):
    """Representa un producto del inventario identificado por código de barras.

    Registra el stock inicial, la cantidad vendida acumulada y el restante
    disponible. El restante se calcula como stock - vendido.

    Attributes:
        nombre: Nombre descriptivo del producto.
        codigo_barras: Identificador único del producto (debe ser único).
        stock: Cantidad total ingresada al inventario.
        vendido: Cantidad vendida acumulada.
        restante: Cantidad disponible actual (stock - vendido).
    """

    nombre = models.CharField(max_length=255)
    codigo_barras = models.CharField(max_length=255, unique=True)
    stock = models.IntegerField(default=0)
    vendido = models.IntegerField(default=0)
    restante = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Retorna la representación legible del artículo de inventario."""
        return self.nombre

    def clean(self) -> None:
        """Valida las reglas de negocio del inventario antes de guardar.

        Raises:
            ValidationError: Si el stock es negativo.
            ValidationError: Si la cantidad vendida es negativa.
            ValidationError: Si la cantidad vendida supera el stock disponible.
        """
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.vendido < 0:
            raise ValidationError("La cantidad vendida no puede ser negativa.")
        if self.vendido > self.stock:
            raise ValidationError("La cantidad vendida no puede ser mayor al stock disponible.")


class Devolucion(models.Model):
    """Representa una devolución de mercadería con imagen de evidencia.

    Attributes:
        imagen: Foto de la mercadería devuelta. Se almacena en media/devoluciones/.
        fecha: Fecha en que se realizó la devolución.
    """

    imagen = models.ImageField(upload_to='devoluciones/')
    fecha = models.DateField()

    def __str__(self) -> str:
        """Retorna la representación legible de la devolución."""
        return f"Devolución {self.id} - {self.fecha}"

    def clean(self) -> None:
        """Valida que la devolución tenga imagen y fecha antes de guardar.

        Raises:
            ValidationError: Si no se proporcionó una imagen.
            ValidationError: Si no se proporcionó una fecha.
        """
        if not self.imagen:
            raise ValidationError("Debe proporcionar una imagen para la devolución.")
        if not self.fecha:
            raise ValidationError("Debe proporcionar una fecha para la devolución.")
