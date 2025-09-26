from django import forms
from .models import InventoryTransaction
from variables.models import Product

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = [
            'product',
            'transaction_type',
            'quantity',
            'location',
            'reference',
            'notes',
            'unit_price',
        ]

        labels = {
            'product': 'Producto',
            'transaction_type': 'Tipo de Transacción',
            'quantity': 'Cantidad',
            'location': 'Ubicación',
            'reference': 'Referencia',
            'notes': 'Notas',
            'unit_price': 'Precio Unitario',
        }
        widgets = {
            'transaction_type': forms.Select(choices=InventoryTransaction.TRANSACTION_TYPES),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

# Mantener compatibilidad con el nombre anterior
MeasurementForm = InventoryTransactionForm
