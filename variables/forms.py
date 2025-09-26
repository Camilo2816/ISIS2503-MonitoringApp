from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'description',
            'category',
            'unit_price',
            'current_stock',
            'min_stock',
            'max_stock',
            'unit',
        ]
        labels = {
            'name': 'Nombre del Producto',
            'sku': 'SKU',
            'description': 'Descripción',
            'category': 'Categoría',
            'unit_price': 'Precio Unitario',
            'current_stock': 'Stock Actual',
            'min_stock': 'Stock Mínimo',
            'max_stock': 'Stock Máximo',
            'unit': 'Unidad',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

# Mantener compatibilidad con el nombre anterior
VariableForm = ProductForm