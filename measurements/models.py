from django.db import models
from variables.models import Product

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
        ('ADJ', 'Ajuste'),
        ('TRF', 'Transferencia'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES, verbose_name="Tipo de Transacción")
    quantity = models.IntegerField(verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Unitario")
    total_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Valor Total")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    notes = models.TextField(blank=True, verbose_name="Notas")
    location = models.CharField(max_length=50, verbose_name="Ubicación")
    user = models.CharField(max_length=50, default="Sistema", verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Transacción")
    
    class Meta:
        verbose_name = "Transacción de Inventario"
        verbose_name_plural = "Transacciones de Inventario"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_transaction_type_display()} - {self.product.name} ({self.quantity} {self.product.unit})'
    
    def save(self, *args, **kwargs):
        # Calcular valor total si no está definido
        if not self.total_value and self.unit_price:
            self.total_value = self.unit_price * self.quantity
        elif not self.unit_price and self.product.unit_price:
            self.unit_price = self.product.unit_price
            self.total_value = self.unit_price * self.quantity
        
        super().save(*args, **kwargs)
        
        # Actualizar stock del producto
        self.update_product_stock()
    
    def update_product_stock(self):
        """Actualiza el stock del producto según el tipo de transacción"""
        if self.transaction_type in ['IN', 'ADJ']:
            # Entrada o ajuste positivo
            self.product.current_stock += self.quantity
        elif self.transaction_type in ['OUT', 'TRF']:
            # Salida o transferencia
            self.product.current_stock -= self.quantity
        
        self.product.save()