from rest_framework import serializers
from .models import Categoria, Producto, Venta, Devolucion

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre']
        read_only_fields = ['id']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio_venta', 'categoria', 'codigo_barras', 'stock', 'stock_minimo']
        read_only_fields = ['id']

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'precio_unitario', 'total', 'fecha', 'anulada', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

class DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devolucion
        fields = ['producto', 'cantidad', 'fecha', 'motivo']
        read_only_fields = ['id',]