from django.contrib import admin
from . models import InventoryTransaction

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'location', 'created_at']
    list_filter = ['transaction_type', 'created_at', 'location']
    search_fields = ['product__name', 'product__sku', 'reference']
    readonly_fields = ['created_at']

