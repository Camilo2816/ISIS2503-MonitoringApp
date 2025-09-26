# 🗄️ Configuración de Amazon RDS PostgreSQL para el Experimento

## 📋 Pasos para crear la instancia RDS

### 1. **Crear instancia RDS PostgreSQL**

```bash
# Usando AWS CLI (opcional)
aws rds create-db-instance \
    --db-instance-identifier inventory-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username postgres \
    --master-user-password TuPasswordSegura123 \
    --allocated-storage 20 \
    --storage-type gp2 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-subnet-group-name default \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted
```

### 2. **Configuración recomendada para el experimento:**

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Instance Class** | `db.t3.micro` | Suficiente para el experimento |
| **Engine** | PostgreSQL 15.4 | Versión estable |
| **Storage** | 20 GB GP2 | Almacenamiento básico |
| **Multi-AZ** | ✅ Habilitado | Alta disponibilidad |
| **Backup** | 7 días | Retención de backups |
| **Encryption** | ✅ Habilitado | Seguridad |

### 3. **Configurar Security Group**

```bash
# Reglas de entrada para PostgreSQL (puerto 5432)
Type: PostgreSQL
Protocol: TCP
Port: 5432
Source: Security Group de las EC2
```

### 4. **Conectar y configurar la base de datos**

```bash
# Conectar desde una EC2
psql -h tu-rds-endpoint.amazonaws.com -U postgres -d postgres

# Ejecutar el script de configuración
\i setup_database.sql
```

## 🔧 **Configuración de Django para RDS**

### Variables de entorno en las EC2:

```bash
# En /opt/inventory-app/.env
DEBUG=False
SECRET_KEY=tu-secret-key-muy-seguro
DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=inventory_password_2024
DB_HOST=tu-rds-endpoint.amazonaws.com
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,tu-alb-dns.amazonaws.com
```

### Configuración en production_settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'inventory_db'),
        'USER': os.environ.get('DB_USER', 'inventory_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'inventory_password_2024'),
        'HOST': os.environ.get('DB_HOST', 'tu-rds-endpoint.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

## 📊 **Monitoreo de RDS**

### Métricas importantes en CloudWatch:
- **CPU Utilization**
- **Database Connections**
- **Read/Write IOPS**
- **Free Storage Space**
- **Replication Lag** (si usas Multi-AZ)

### Consultas útiles para monitoreo:

```sql
-- Ver conexiones activas
SELECT count(*) FROM pg_stat_activity;

-- Ver consultas más lentas
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Ver tamaño de la base de datos
SELECT pg_size_pretty(pg_database_size('inventory_db'));
```

## 🚀 **Ventajas de usar RDS para el experimento:**

1. **✅ Alta Disponibilidad**: Multi-AZ garantiza uptime
2. **✅ Escalabilidad**: Fácil cambio de instancia class
3. **✅ Backups Automáticos**: Recuperación ante fallos
4. **✅ Monitoreo**: Métricas detalladas en CloudWatch
5. **✅ Seguridad**: Encriptación en tránsito y reposo
6. **✅ Mantenimiento**: Patches automáticos

## 💰 **Costo estimado para el experimento:**

- **db.t3.micro**: ~$15-20/mes
- **Storage 20GB**: ~$2-3/mes
- **Total**: ~$17-23/mes

## 🔍 **Troubleshooting común:**

### Error de conexión:
```bash
# Verificar conectividad
telnet tu-rds-endpoint.amazonaws.com 5432

# Verificar DNS
nslookup tu-rds-endpoint.amazonaws.com
```

### Error de SSL:
```python
# En Django settings
'OPTIONS': {
    'sslmode': 'require',  # o 'prefer' para desarrollo
}
```

### Error de permisos:
```sql
-- Verificar usuario
SELECT usename FROM pg_user WHERE usename = 'inventory_user';

-- Verificar permisos
\du inventory_user
```

## 📝 **Checklist de configuración:**

- [ ] Instancia RDS creada
- [ ] Security Group configurado
- [ ] Base de datos y usuario creados
- [ ] Conectividad desde EC2 verificada
- [ ] Variables de entorno configuradas
- [ ] Migraciones de Django ejecutadas
- [ ] Monitoreo en CloudWatch habilitado
