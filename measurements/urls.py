from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # Vistas web (mantener compatibilidad)
    path('measurements/', views.transaction_list),
    path('measurementcreate/', csrf_exempt(views.transaction_create), name='transactionCreate'),
    
    # API endpoints para el sistema de inventario
    path('inventory/transactions', views.inventory_transactions_api, name='inventory_transactions_api'),
    path('inventory/transactions/create', views.inventory_transaction_create_api, name='inventory_transaction_create_api'),
    path('inventory/summary', views.inventory_summary_api, name='inventory_summary_api'),
    path('products', views.products_api, name='products_api'),
    
    # Endpoints legacy para compatibilidad con el experimento
    path('measurements', views.inventory_transactions_api, name='measurements_api'),
    path('measurements/create', views.inventory_transaction_create_api, name='measurements_create_api'),
]