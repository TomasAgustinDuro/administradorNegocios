from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import DiarioVendido, Inventario, Devolucion
import json

# Vista para DiarioVendido
@csrf_exempt
@require_http_methods(["GET", "POST"])
def diario_vendido_list(request):
    if request.method == 'GET':
        diarios = DiarioVendido.objects.all()
        data = list(diarios.values('id', 'nombre', 'valor'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        body = json.loads(request.body)
        nuevo_diario = DiarioVendido.objects.create(
            nombre=body['nombre'],
            valor=body['valor']
        )
        return JsonResponse({
            'id': nuevo_diario.id,
            'nombre': nuevo_diario.nombre,
            'valor': nuevo_diario.valor
        })

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def diario_vendido_detail(request, pk):
    try:
        diario = DiarioVendido.objects.get(pk=pk)
    except DiarioVendido.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        data = {
            'id': diario.id,
            'nombre': diario.nombre,
            'valor': diario.valor
        }
        return JsonResponse(data)
    
    if request.method == 'PUT':
        body = json.loads(request.body)
        diario.nombre = body['nombre']
        diario.valor = body['valor']
        diario.save()
        return JsonResponse({
            'id': diario.id,
            'nombre': diario.nombre,
            'valor': diario.valor
        })
    
    if request.method == 'DELETE':
        diario.delete()
        return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_ventas(request):
    DiarioVendido.objects.all().delete()
    return HttpResponse(status=204)

# Vista para Inventario
@csrf_exempt
@require_http_methods(["GET", "POST"])
def inventario_list(request):
    if request.method == 'GET':
        inventarios = Inventario.objects.all()
        data = list(inventarios.values('id', 'nombre', 'codigo_barras', 'stock', 'vendido', 'restante'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        body = json.loads(request.body)
        nuevo_inventario = Inventario.objects.create(
            nombre=body['nombre'],
            codigo_barras=body['codigo_barras'],
            stock = body['stock'],            
            vendido = body ['vendido'],
            restante = int(body.get('stock')) - int(body ['vendido'])
        )
        return JsonResponse({
            'id': nuevo_inventario.id,
            'nombre': nuevo_inventario.nombre,
            'codigo_barras': nuevo_inventario.codigo_barras,    
            'stock':nuevo_inventario.stock,
            'vendido':nuevo_inventario.vendido
        })

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def inventario_detail(request, pk):
    try:
        inventario = Inventario.objects.get(pk=pk)
    except Inventario.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        restante = inventario.stock - inventario.vendido 
        data = {
            'id': inventario.id,
            'nombre': inventario.nombre,
            'codigo_barras': inventario.codigo_barras,
            'numero_identificador': inventario.numero_identificador,
            'stock': inventario.stock,
            'vendido': inventario.vendido,
            'restante': restante
        }
        return JsonResponse(data)
    
    if request.method == 'PUT':
        body = json.loads(request.body)
        inventario.nombre = body['nombre']
        inventario.codigo_barras = body['codigo_barras']
        inventario.numero_identificador = body['numero_identificador']
        inventario.stock = body.get('stock', inventario.stock)
        inventario.vendido = body.get('vendido', inventario.vendido)
        inventario.save()
        restante = inventario.stock - inventario.vendido 
        
        return JsonResponse({
            'id': inventario.id,
            'nombre': inventario.nombre,
            'codigo_barras': inventario.codigo_barras,
            'numero_identificador': inventario.numero_identificador,
            'stock': inventario.stock,
            'vendido': inventario.vendido,
            'restante': restante
        })
    
    if request.method == 'DELETE':
        inventario.delete()
        return HttpResponse(status=204)

# Vista para Devolucion
@csrf_exempt
@require_http_methods(["GET", "POST"])
def devolucion_list(request):
    if request.method == 'GET':
        devoluciones = Devolucion.objects.all()
        data = list(devoluciones.values('id', 'imagen', 'fecha'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        body = json.loads(request.body)
        # Asumimos que la imagen se sube de una manera adecuada, pero se omite para simplificar
        nueva_devolucion = Devolucion.objects.create(
            imagen=body['imagen'],
            fecha=body['fecha']
        )
        return JsonResponse({
            'id': nueva_devolucion.id,
            'imagen': nueva_devolucion.imagen.url,  # Obtén la URL de la imagen
            'fecha': nueva_devolucion.fecha
        })

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def devolucion_detail(request, pk):
    try:
        devolucion = Devolucion.objects.get(pk=pk)
    except Devolucion.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        data = {
            'id': devolucion.id,
            'imagen': devolucion.imagen.url,
            'fecha': devolucion.fecha
        }
        return JsonResponse(data)
    
    if request.method == 'PUT':
        body = json.loads(request.body)
        devolucion.imagen = body['imagen']  # Deberías manejar la carga de archivos adecuadamente
        devolucion.fecha = body['fecha']
        devolucion.save()
        return JsonResponse({
            'id': devolucion.id,
            'imagen': devolucion.imagen.url,
            'fecha': devolucion.fecha
        })
    
    if request.method == 'DELETE':
        devolucion.delete()
        return HttpResponse(status=204)
