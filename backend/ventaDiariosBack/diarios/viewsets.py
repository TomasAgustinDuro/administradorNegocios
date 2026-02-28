from rest_framework import viewsets, status, filters
from .models import Categoria, Producto, Venta, Devolucion
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    VentaSerializer,
    DevolucionSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nombre']
    search_fields = ['nombre']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['categoria', 'codigo_barras', 'nombre']
    ordering_fields = ['nombre', 'stock', 'precio_venta']
    search_fields = ['nombre', 'codigo_barras', 'categoria']

    ordering = ['nombre']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fecha', 'producto', 'anulada'] 

    ordering_fields = ['fecha', 'cantidad', 'created_at']

    ordering = ['fecha']

    @action(detail=True, methods=['post'])
    def anular(self, request, pk=None):
        venta = self.get_object()

        if not venta.anulada:
            venta.anular()

            return Response({'status': 'Venta anulada exitosamente'}, status=status.HTTP_200_OK)


class DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Devolucion.objects.all()
    serializer_class = DevolucionSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fecha', 'producto', 'motivo'] 

    ordering_fields = ['fecha', 'producto']

    ordering = ['fecha']