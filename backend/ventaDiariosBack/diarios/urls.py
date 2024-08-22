from django.urls import path
from .views import diario_vendido_list, diario_vendido_detail, eliminar_ventas, inventario_list, inventario_detail, devolucion_list, devolucion_detail


urlpatterns = [
    path('api/diarios/', diario_vendido_list, name='diario-list'),
    path('api/diarios/<int:pk>/', diario_vendido_detail, name='diario-detail'),
    path('api/diarios/eliminar_todos/', eliminar_ventas, name='diario-eliminar-todo'),
    path('api/inventarios/', inventario_list, name='inventario-list'),
    path('api/inventarios/<int:pk>/', inventario_detail, name='inventario-detail'),
    path('api/devoluciones/', devolucion_list, name='devolucion-list'),
    path('api/devoluciones/<int:pk>/', devolucion_detail, name='devolucion-detail'),
]


