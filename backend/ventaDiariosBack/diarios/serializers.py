from rest_framework import serializers
from .models import Categoria, Producto, Venta, Devolucion
import re
from datetime import date

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_venta', 'categoria', 'codigo_barras', 'stock', 'stock_minimo']
        read_only_fields = ['id']

    def validate_precio_venta(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser menor que 0")
        return value

    def validate_codigo_barras(self, value):
        if not re.match(r"^\d{8,13}$", value):
            raise serializers.ValidationError("El código de barras debe tener entre 8 y 13 dígitos numéricos")
        return value

    def validate_nombre(self, value):
        if not re.match(r"^[a-zA-Z0-9\s]+$", value):
            raise serializers.ValidationError("El nombre solo puede contener letras, números y espacios.")
        return value

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'total', 'fecha', 'anulada', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value

    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value

    def validate_fecha(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura")
        return value

    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']

        if cantidad > producto.stock:
            raise serializers.ValidationError("No hay suficiente stock disponible")
        
        return data

class DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devolucion
        fields = ['id', 'producto', 'cantidad', 'fecha', 'motivo']
        read_only_fields = ['id']

    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value

    def validate_motivo(self, value):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.,]+$", value):
            raise serializers.ValidationError("El motivo contiene caracteres no permitidos")
        if len(value) < 10:
            raise serializers.ValidationError("El motivo debe tener al menos 10 caracteres")
        return value

    def validate_fecha(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura")
        return value
