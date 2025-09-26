from ..models import Product
from django.db import models

def get_products():
    """Obtiene todos los productos"""
    queryset = Product.objects.all()
    return queryset

def get_product_by_id(product_id):
    """Obtiene un producto por ID"""
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

def create_product(form):
    """Crea un nuevo producto"""
    product = form.save()
    product.save()
    return product

def update_product_stock(product_id, new_stock):
    """Actualiza el stock de un producto"""
    try:
        product = Product.objects.get(id=product_id)
        product.current_stock = new_stock
        product.save()
        return product
    except Product.DoesNotExist:
        return None

def get_low_stock_products():
    """Obtiene productos con stock bajo"""
    return Product.objects.filter(current_stock__lte=models.F('min_stock'))

def get_out_of_stock_products():
    """Obtiene productos agotados"""
    return Product.objects.filter(current_stock__lte=0)

# Mantener compatibilidad con nombres anteriores
get_variables = get_products
create_variable = create_product