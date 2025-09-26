from django.shortcuts import render
from .forms import MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .logic.logic_measurement import create_transaction, get_transactions, get_inventory_summary
from variables.models import Product
import json

def transaction_list(request):
    """Vista para listar transacciones de inventario"""
    transactions = get_transactions()
    context = {
        'transaction_list': transactions
    }
    return render(request, 'Measurement/measurements.html', context)

def transaction_create(request):
    """Vista para crear transacciones de inventario"""
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            create_transaction(form.cleaned_data)
            messages.add_message(request, messages.SUCCESS, 'Transacción creada exitosamente')
            return HttpResponseRedirect(reverse('transactionCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)

# API REST endpoints para el sistema de inventario
@csrf_exempt
@require_http_methods(["GET"])
def inventory_transactions_api(request):
    """API endpoint GET /inventory/transactions - Lista las últimas transacciones de inventario"""
    try:
        transactions = get_transactions()
        data = []
        for transaction in transactions:
            data.append({
                'id': transaction.id,
                'product': {
                    'id': transaction.product.id,
                    'name': transaction.product.name,
                    'sku': transaction.product.sku
                },
                'transaction_type': transaction.get_transaction_type_display(),
                'quantity': transaction.quantity,
                'unit_price': float(transaction.unit_price) if transaction.unit_price else None,
                'total_value': float(transaction.total_value) if transaction.total_value else None,
                'reference': transaction.reference,
                'location': transaction.location,
                'user': transaction.user,
                'created_at': transaction.created_at.isoformat()
            })
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def inventory_transaction_create_api(request):
    """API endpoint POST /inventory/transactions/create - Crea una nueva transacción de inventario"""
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        required_fields = ['product_id', 'transaction_type', 'quantity', 'location']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Campo requerido: {field}'
                }, status=400)
        
        # Validar tipo de transacción
        valid_types = ['IN', 'OUT', 'ADJ', 'TRF']
        if data['transaction_type'] not in valid_types:
            return JsonResponse({
                'status': 'error',
                'message': f'Tipo de transacción inválido. Debe ser uno de: {", ".join(valid_types)}'
            }, status=400)
        
        # Obtener producto
        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Producto no encontrado'
            }, status=404)
        
        # Crear transacción
        transaction_data = {
            'product': product,
            'transaction_type': data['transaction_type'],
            'quantity': data['quantity'],
            'location': data['location'],
            'reference': data.get('reference', ''),
            'notes': data.get('notes', ''),
            'user': data.get('user', 'Sistema'),
            'unit_price': data.get('unit_price'),
            'total_value': data.get('total_value')
        }
        
        transaction = create_transaction(transaction_data)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Transacción creada exitosamente',
            'data': {
                'id': transaction.id,
                'product': {
                    'id': transaction.product.id,
                    'name': transaction.product.name,
                    'sku': transaction.product.sku,
                    'current_stock': transaction.product.current_stock
                },
                'transaction_type': transaction.get_transaction_type_display(),
                'quantity': transaction.quantity,
                'unit_price': float(transaction.unit_price) if transaction.unit_price else None,
                'total_value': float(transaction.total_value) if transaction.total_value else None,
                'location': transaction.location,
                'created_at': transaction.created_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def inventory_summary_api(request):
    """API endpoint GET /inventory/summary - Obtiene resumen del inventario"""
    try:
        summary = get_inventory_summary()
        return JsonResponse({
            'status': 'success',
            'data': summary
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def products_api(request):
    """API endpoint GET /products - Lista todos los productos"""
    try:
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'description': product.description,
                'category': product.category,
                'unit_price': float(product.unit_price),
                'current_stock': product.current_stock,
                'min_stock': product.min_stock,
                'max_stock': product.max_stock,
                'unit': product.unit,
                'is_low_stock': product.is_low_stock(),
                'is_out_of_stock': product.is_out_of_stock(),
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat()
            })
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)