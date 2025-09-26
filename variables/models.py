from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    description = models.TextField(blank=True, verbose_name="Descripción")
    category = models.CharField(max_length=50, verbose_name="Categoría")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    current_stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    min_stock = models.IntegerField(default=0, verbose_name="Stock Mínimo")
    max_stock = models.IntegerField(default=1000, verbose_name="Stock Máximo")
    unit = models.CharField(max_length=20, default="unidades", verbose_name="Unidad")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} (SKU: {self.sku})'
    
    def is_low_stock(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.current_stock <= self.min_stock
    
    def is_out_of_stock(self):
        """Verifica si el producto está agotado"""
        return self.current_stock <= 0

