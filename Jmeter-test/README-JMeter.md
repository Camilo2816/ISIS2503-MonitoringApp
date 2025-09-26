# 🧪 Guía de Pruebas JMeter - Sistema de Inventario

## 📋 Archivos de Configuración

### 1. **Local-Test.jmx** - Para pruebas locales
- **Host**: 127.0.0.1:8000
- **Usuarios**: 10 concurrentes
- **Duración**: 5 loops por usuario
- **Propósito**: Probar la aplicación localmente

### 2. **Inventory-Load-Test.jmx** - Para el experimento AWS
- **Host**: tu-alb-dns.amazonaws.com
- **Usuarios**: 70 concurrentes total
- **Duración**: Múltiples loops
- **Propósito**: Simular carga real en ALB + EC2

## 🚀 Cómo Ejecutar las Pruebas

### **Pruebas Locales (Desarrollo)**

1. **Asegúrate de que Django esté ejecutándose:**
```bash
cd ISIS2503-MonitoringApp
python manage.py runserver
```

2. **Abre JMeter:**
```bash
jmeter
```

3. **Carga el archivo:**
- File → Open → `Local-Test.jmx`

4. **Ejecuta la prueba:**
- Click en "Start" (▶️)

### **Pruebas en AWS (Experimento)**

1. **Configura las variables:**
   - Cambia `ALB_DNS` por tu DNS real del ALB
   - Ajusta `PORT` si es necesario (80 o 443)

2. **Ejecuta la prueba:**
   - File → Open → `Inventory-Load-Test.jmx`
   - Click en "Start" (▶️)

## 📊 Grupos de Pruebas

### **🏥 Health Check Group**
- **Usuarios**: 5
- **Loops**: 10
- **Endpoint**: `GET /health-check/`
- **Propósito**: Simular health checks del ALB

### **📦 Product Operations Group**
- **Usuarios**: 20
- **Loops**: 5
- **Endpoint**: `GET /products`
- **Propósito**: Consultar productos disponibles

### **🔄 Transaction Operations Group**
- **Usuarios**: 30
- **Loops**: 3
- **Endpoints**: 
  - `POST /inventory/transactions/create` (Entrada)
  - `POST /inventory/transactions/create` (Salida)
- **Propósito**: Simular operaciones de bodega

### **📊 Transaction Queries Group**
- **Usuarios**: 15
- **Loops**: 8
- **Endpoints**:
  - `GET /inventory/transactions`
  - `GET /inventory/summary`
- **Propósito**: Consultar transacciones y resúmenes

## 🎯 Escenarios de Prueba

### **Escenario 1: Operaciones Normales**
```
Health Check: 10% del tráfico
Productos: 20% del tráfico
Transacciones: 50% del tráfico
Consultas: 20% del tráfico
```

### **Escenario 2: Carga Alta**
```
Transacciones: 80% del tráfico
Consultas: 15% del tráfico
Health Check: 5% del tráfico
```

## 📈 Métricas a Monitorear

### **Performance Metrics:**
- **Response Time**: Tiempo de respuesta promedio
- **Throughput**: Transacciones por segundo
- **Error Rate**: Porcentaje de errores
- **95th Percentile**: Tiempo de respuesta del 95%

### **Load Balancing Metrics:**
- **Distribution**: ¿Se distribuye uniformemente?
- **Health Check Success**: ¿ALB detecta EC2 saludables?
- **Connection Pool**: Uso de conexiones

## 🔧 Configuración Avanzada

### **Variables de Entorno:**
```bash
# Para pruebas locales
HOST=127.0.0.1
PORT=8000

# Para pruebas AWS
ALB_DNS=tu-alb-dns.amazonaws.com
PORT=80
PROTOCOL=http
```

### **Parámetros de Carga:**
- **Ramp-up Time**: Tiempo para alcanzar usuarios máximos
- **Loop Count**: Número de iteraciones por usuario
- **Duration**: Duración total de la prueba

## 📊 Resultados Esperados

### **Respuestas Exitosas:**
- **Health Check**: 200 OK
- **Products**: 200 OK con JSON de productos
- **Transactions**: 200 OK con JSON de transacciones
- **Create Transaction**: 200 OK con datos de la transacción

### **Métricas de Rendimiento:**
- **Response Time**: < 500ms (objetivo)
- **Throughput**: > 10 TPS (transacciones por segundo)
- **Error Rate**: < 1%

## 🚨 Troubleshooting

### **Error: Connection Refused**
- Verifica que Django esté ejecutándose
- Verifica la URL y puerto

### **Error: 404 Not Found**
- Verifica que los endpoints estén configurados
- Revisa las URLs en el archivo JMeter

### **Error: 500 Internal Server Error**
- Revisa los logs de Django
- Verifica que la base de datos esté configurada

## 📝 Ejemplo de Uso

### **1. Preparar datos de prueba:**
```bash
# Crear productos en el admin
# http://127.0.0.1:8000/admin/
```

### **2. Ejecutar prueba local:**
```bash
jmeter -n -t Local-Test.jmx -l results/local-results.jtl
```

### **3. Ver resultados:**
```bash
jmeter -g results/local-results.jtl -o results/report/
```

## 🎯 Objetivos del Experimento

1. **Demostrar balanceo de carga** entre EC2
2. **Medir latencia** de cada endpoint
3. **Verificar health checks** del ALB
4. **Simular operaciones reales** de bodega
5. **Comparar algoritmos** de distribución (Round Robin vs Least Connections)

## 📊 Reportes

Los resultados se guardan en:
- `results/local-results.jtl` - Pruebas locales
- `results/summary-report.jtl` - Resumen de métricas
- `results/graph-results.jtl` - Gráficos de rendimiento

¡Listo para probar tu sistema de inventario! 🚀
