from rest_framework import viewsets
from .models import Categoria, Producto, Venta, Devolucion
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    VentaSerializer,
    DevolucionSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fecha', 'producto', 'anulada'] 

class DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Devolucion.objects.all()
    serializer_class = DevolucionSerializer