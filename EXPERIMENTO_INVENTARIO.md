# 🏭 Sistema de Inventario de Bodega - Experimento ALB + EC2

## 📋 Descripción del Experimento

Este proyecto implementa un sistema de inventario de bodega distribuido usando:
- **Application Load Balancer (ALB)** como punto de entrada
- **2 instancias EC2** ejecutando Django con Gunicorn
- **Base de datos PostgreSQL (RDS)** centralizada
- **JMeter** para pruebas de carga

## 🏗️ Arquitectura

```
Cliente/JMeter → ALB → EC2-1 (Django/Gunicorn:8080)
                      → EC2-2 (Django/Gunicorn:8080)
                      → RDS PostgreSQL
```

## 🚀 Endpoints Disponibles

### Health Check (para ALB)
- **GET** `/health-check/` - Verificación de salud del servicio

### API de Inventario
- **GET** `/inventory/transactions` - Lista transacciones de inventario
- **POST** `/inventory/transactions/create` - Crea nueva transacción
- **GET** `/inventory/summary` - Resumen del inventario
- **GET** `/products` - Lista todos los productos

### Endpoints Legacy (compatibilidad)
- **GET** `/measurements` - Alias para transacciones
- **POST** `/measurements/create` - Alias para crear transacción

## 📊 Modelos de Datos

### Product (Producto)
- `name`: Nombre del producto
- `sku`: Código único del producto
- `description`: Descripción
- `category`: Categoría
- `unit_price`: Precio unitario
- `current_stock`: Stock actual
- `min_stock`: Stock mínimo
- `max_stock`: Stock máximo
- `unit`: Unidad de medida

### InventoryTransaction (Transacción)
- `product`: Producto relacionado
- `transaction_type`: Tipo (IN/OUT/ADJ/TRF)
- `quantity`: Cantidad
- `unit_price`: Precio unitario
- `total_value`: Valor total
- `reference`: Referencia
- `location`: Ubicación
- `user`: Usuario
- `created_at`: Fecha de creación

## 🔧 Configuración del Experimento

### 1. Configurar RDS PostgreSQL
```sql
-- Ejecutar setup_database.sql en RDS
CREATE DATABASE inventory_db;
CREATE USER inventory_user WITH PASSWORD 'inventory_password_2024';
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;
```

### 2. Desplegar en EC2
```bash
# En cada instancia EC2
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

### 3. Configurar ALB
- **Target Group**: Puerto 8080
- **Health Check**: `/health-check/`
- **Algoritmos a probar**:
  - Round Robin (por defecto)
  - Least Connections

### 4. Configurar JMeter
- Usar `Load-tests.jmx` existente
- Modificar endpoints para usar `/inventory/transactions`
- Configurar carga para simular operaciones de bodega

## 📈 Escenarios de Prueba

### Escenario 1: Round Robin
- ALB distribuye tráfico uniformemente entre EC2
- Verificar balanceo de carga
- Medir latencia y throughput

### Escenario 2: Least Connections
- ALB envía tráfico a EC2 con menos conexiones
- Comparar rendimiento vs Round Robin
- Analizar distribución de carga

### Operaciones de Inventario a Simular
1. **Entrada de productos** (IN)
2. **Salida de productos** (OUT)
3. **Ajustes de inventario** (ADJ)
4. **Transferencias** (TRF)
5. **Consultas de stock**

## 🧪 Ejemplos de Uso

### Crear una transacción de entrada
```bash
curl -X POST http://tu-alb-dns/inventory/transactions/create \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "transaction_type": "IN",
    "quantity": 100,
    "location": "Bodega A",
    "reference": "PO-2024-001",
    "notes": "Compra de productos"
  }'
```

### Consultar transacciones
```bash
curl http://tu-alb-dns/inventory/transactions
```

### Verificar salud del servicio
```bash
curl http://tu-alb-dns/health-check/
```

## 📝 Notas Importantes

1. **Base de datos compartida**: Ambas EC2 usan la misma RDS
2. **Consistencia**: Las transacciones actualizan automáticamente el stock
3. **Health checks**: ALB verifica `/health-check/` cada 30 segundos
4. **Logs**: Revisar logs en `/opt/inventory-app/logs/`
5. **Monitoreo**: Usar CloudWatch para métricas de ALB y EC2

## 🔍 Troubleshooting

### Verificar servicios
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### Verificar logs
```bash
tail -f /opt/inventory-app/logs/django.log
```

### Verificar conectividad a RDS
```bash
psql -h tu-rds-endpoint -U inventory_user -d inventory_db
```

## 📊 Métricas a Medir

1. **Latencia**: Tiempo de respuesta de endpoints
2. **Throughput**: Transacciones por segundo
3. **Balanceo**: Distribución de carga entre EC2
4. **Disponibilidad**: Uptime del sistema
5. **Escalabilidad**: Comportamiento bajo carga

## 🎯 Objetivos del Experimento

- Demostrar balanceo de carga con ALB
- Comparar algoritmos de distribución
- Simular operaciones reales de bodega
- Medir rendimiento y escalabilidad
- Validar arquitectura distribuida
