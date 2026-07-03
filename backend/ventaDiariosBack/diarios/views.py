from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import DiarioVendido, Inventario, Devolucion
import json


# Vista para DiarioVendido
@csrf_exempt
@require_http_methods(["GET", "POST"])
def diario_vendido_list(request: object) -> JsonResponse:
    """Lista todos los diarios vendidos o crea uno nuevo.

    GET: Retorna todos los registros de DiarioVendido.
    POST: Crea un nuevo registro validando nombre y valor.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        JsonResponse con la lista de diarios (GET) o el nuevo registro (POST).
        Status 400 si faltan campos requeridos o hay errores de validación.
    """
    if request.method == 'GET':
        diarios = DiarioVendido.objects.all()
        data = list(diarios.values('id', 'nombre', 'valor'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            nombre = body.get('nombre')
            valor = body.get('valor')
            if not nombre or not valor:
                return JsonResponse({"error": "El nombre y el valor son requeridos."}, status=400)
            nuevo_diario = DiarioVendido(nombre=nombre, valor=valor)
            nuevo_diario.clean()
            nuevo_diario.save()
            return JsonResponse({
                'id': nuevo_diario.id,
                'nombre': nuevo_diario.nombre,
                'valor': nuevo_diario.valor
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def diario_vendido_detail(request: object, pk: int) -> JsonResponse | HttpResponse:
    """Recupera, actualiza o elimina un diario vendido por su ID.

    Args:
        request: Objeto HttpRequest de Django.
        pk: Clave primaria del registro DiarioVendido a operar.

    Returns:
        JsonResponse con los datos del diario (GET/PUT).
        HttpResponse 204 al eliminar exitosamente.
        HttpResponse 404 si el registro no existe.
        JsonResponse con error 400 si la validación falla.
    """
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
        try:
            body = json.loads(request.body)
            nombre = body.get('nombre')
            valor = body.get('valor')
            if nombre:
                diario.nombre = nombre
            if valor:
                diario.valor = valor
            diario.clean()
            diario.save()
            return JsonResponse({
                'id': diario.id,
                'nombre': diario.nombre,
                'valor': diario.valor
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    if request.method == 'DELETE':
        diario.delete()
        return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_ventas(request: object) -> HttpResponse:
    """Elimina todos los registros de DiarioVendido de la base de datos.

    Permite al operador limpiar el registro de ventas al cierre del día.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        HttpResponse 204 sin contenido tras borrar todos los registros.
    """
    DiarioVendido.objects.all().delete()
    return HttpResponse(status=204)


# Vista para Inventario
@csrf_exempt
@require_http_methods(["GET", "POST"])
def inventario_list(request: object) -> JsonResponse:
    """Lista todos los artículos del inventario o crea uno nuevo.

    GET: Retorna todos los artículos con su stock, vendido y restante.
    POST: Crea un nuevo artículo validando nombre, código de barras y cantidades.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        JsonResponse con la lista de artículos (GET) o el nuevo artículo (POST).
        Status 400 si faltan campos requeridos o hay errores de validación.
    """
    if request.method == 'GET':
        inventarios = Inventario.objects.all()
        data = list(inventarios.values('id', 'nombre', 'codigo_barras', 'stock', 'vendido', 'restante'))
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            nombre = body.get('nombre')
            codigo_barras = body.get('codigo_barras')
            stock = int(body.get('stock', 0))
            vendido = int(body.get('vendido', 0))

            if not nombre or not codigo_barras:
                return JsonResponse({"error": "El nombre y el código de barras son requeridos."}, status=400)

            nuevo_inventario = Inventario(
                nombre=nombre,
                codigo_barras=codigo_barras,
                stock=stock,
                vendido=vendido,
                restante=stock - vendido
            )
            nuevo_inventario.clean()
            nuevo_inventario.save()
            return JsonResponse({
                'id': nuevo_inventario.id,
                'nombre': nuevo_inventario.nombre,
                'codigo_barras': nuevo_inventario.codigo_barras,
                'stock': nuevo_inventario.stock,
                'vendido': nuevo_inventario.vendido,
                'restante': nuevo_inventario.restante
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def inventario_detail(request: object, pk: int) -> JsonResponse | HttpResponse:
    """Recupera, actualiza o elimina un artículo de inventario por su ID.

    En el método PUT, el campo 'vendido' es incremental: se suma al valor
    existente en lugar de reemplazarlo.

    Args:
        request: Objeto HttpRequest de Django.
        pk: Clave primaria del artículo de Inventario a operar.

    Returns:
        JsonResponse con los datos del artículo (GET/PUT).
        HttpResponse 204 al eliminar exitosamente.
        HttpResponse 404 si el artículo no existe.
        JsonResponse con error 400 si la validación falla.
    """
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
            'stock': inventario.stock,
            'vendido': inventario.vendido,
            'restante': restante
        }
        return JsonResponse(data)
    
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            if 'nombre' in body:
                inventario.nombre = body['nombre']
            if 'codigo_barras' in body:
                inventario.codigo_barras = body['codigo_barras']
            if 'stock' in body:
                inventario.stock = int(body['stock'])
            if 'vendido' in body:
                vendido = int(body['vendido'])
                inventario.vendido += vendido
            restante = inventario.stock - inventario.vendido
            inventario.restante = restante
            inventario.clean()
            inventario.save()
            return JsonResponse({
                'id': inventario.id,
                'nombre': inventario.nombre,
                'codigo_barras': inventario.codigo_barras,
                'stock': inventario.stock,
                'vendido': inventario.vendido,
                'restante': restante
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    if request.method == 'DELETE':
        inventario.delete()
        return HttpResponse(status=204)

# Vista para Devolucion
@csrf_exempt
@require_http_methods(["GET", "POST"])
def devolucion_list(request: object) -> JsonResponse:
    """Lista todas las devoluciones registradas o crea una nueva.

    GET: Retorna todas las devoluciones con su imagen (URL relativa) y fecha.
    POST: Crea una nueva devolución esperando multipart/form-data con
          los campos 'imagen' (archivo) y 'fecha' (string de fecha).

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        JsonResponse con la lista de devoluciones (GET) o la nueva devolución (POST).
        Status 400 si faltan campos requeridos o hay errores de validación.
    """
    if request.method == 'GET':
        devoluciones = Devolucion.objects.all()
        data = [{
            'id': devolucion.id,
            'imagen': devolucion.imagen.url,
            'fecha': devolucion.fecha
        }for devolucion in devoluciones]
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        try:
            imagen = request.FILES.get('imagen')
            fecha = request.POST.get('fecha')
            if not imagen or not fecha:
                return JsonResponse({"error": "Imagen y fecha son requeridos."}, status=400)
            nueva_devolucion = Devolucion(imagen=imagen, fecha=fecha)
            nueva_devolucion.clean()
            nueva_devolucion.save()
            return JsonResponse({
                'id': nueva_devolucion.id,
                'imagen': nueva_devolucion.imagen.url,
                'fecha': nueva_devolucion.fecha
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def devolucion_detail(request: object, pk: int) -> JsonResponse | HttpResponse:
    """Recupera, actualiza o elimina una devolución por su ID.

    El método PUT solo permite actualizar la fecha. La imagen no es modificable
    una vez creada la devolución.

    Args:
        request: Objeto HttpRequest de Django.
        pk: Clave primaria de la Devolucion a operar.

    Returns:
        JsonResponse con los datos de la devolución (GET/PUT).
        HttpResponse 204 al eliminar exitosamente.
        HttpResponse 404 si la devolución no existe.
        JsonResponse con error 400 si la validación falla.
    """
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
        try:
            body = json.loads(request.body)
            if 'fecha' in body:
                devolucion.fecha = body['fecha']
            devolucion.clean()
            devolucion.save()
            return JsonResponse({
                'id': devolucion.id,
                'imagen': devolucion.imagen.url,
                'fecha': devolucion.fecha
            })
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    if request.method == 'DELETE':
        devolucion.delete()
        return HttpResponse(status=204)
