from ..models import InventoryTransaction
from variables.models import Product
from django.db import models

def get_transactions():
    """Obtiene las últimas 20 transacciones de inventario"""
    queryset = InventoryTransaction.objects.all().order_by('-created_at')[:20]
    return queryset

def get_transactions_by_product(product_id):
    """Obtiene transacciones de un producto específico"""
    queryset = InventoryTransaction.objects.filter(product_id=product_id).order_by('-created_at')
    return queryset

def create_transaction(transaction_data):
    """Crea una nueva transacción de inventario"""
    transaction = InventoryTransaction.objects.create(**transaction_data)
    return transaction

def get_low_stock_products():
    """Obtiene productos con stock bajo"""
    return Product.objects.filter(current_stock__lte=models.F('min_stock'))

def get_out_of_stock_products():
    """Obtiene productos agotados"""
    return Product.objects.filter(current_stock__lte=0)

def get_inventory_summary():
    """Obtiene resumen del inventario"""
    from django.db.models import Sum, Count
    
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(current_stock__lte=models.F('min_stock')).count()
    out_of_stock_count = Product.objects.filter(current_stock__lte=0).count()
    
    # Calcular valor total del inventario
    total_value = Product.objects.aggregate(
        total=Sum(models.F('current_stock') * models.F('unit_price'))
    )['total'] or 0
    
    return {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_inventory_value': total_value
    }