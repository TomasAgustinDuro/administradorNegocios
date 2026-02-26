from rest_framework.routers import DefaultRouter
from .viewsets import CategoriaViewSet, ProductoViewSet, VentaViewSet, DevolucionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'devoluciones', DevolucionViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]