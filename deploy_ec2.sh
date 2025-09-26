#!/bin/bash

# Script de despliegue para instancias EC2 - Sistema de Inventario
# Este script debe ejecutarse en cada instancia EC2

echo "🚀 Iniciando despliegue del sistema de inventario..."

# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependencias del sistema
sudo apt-get install -y python3 python3-pip python3-venv postgresql-client nginx

# Crear directorio de la aplicación
sudo mkdir -p /opt/inventory-app
sudo chown ubuntu:ubuntu /opt/inventory-app
cd /opt/inventory-app

# Clonar repositorio (ajustar URL según tu repositorio)
# git clone https://github.com/tu-usuario/ISIS2503-MonitoringApp.git .

# O si ya tienes el código, copiarlo aquí
# cp -r /path/to/ISIS2503-MonitoringApp/* .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variables de entorno
cat > .env << EOF
DEBUG=False
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://usuario:password@rds-endpoint:5432/inventory_db
ALLOWED_HOSTS=localhost,127.0.0.1,tu-alb-dns.amazonaws.com
EOF

# Configurar base de datos
python manage.py migrate
python manage.py collectstatic --noinput

# Crear superusuario (opcional)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Configurar Gunicorn
cat > gunicorn.service << EOF
[Unit]
Description=Gunicorn instance to serve inventory app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/opt/inventory-app
Environment="PATH=/opt/inventory-app/venv/bin"
ExecStart=/opt/inventory-app/venv/bin/gunicorn --config gunicorn.conf.py monitoring.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Instalar servicio Gunicorn
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Configurar Nginx como proxy reverso
sudo cat > /etc/nginx/sites-available/inventory-app << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /opt/inventory-app/static/;
    }
}
EOF

# Habilitar sitio Nginx
sudo ln -s /etc/nginx/sites-available/inventory-app /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 8080
sudo ufw --force enable

# Verificar servicios
sudo systemctl status gunicorn
sudo systemctl status nginx

echo "✅ Despliegue completado!"
echo "🌐 Aplicación disponible en: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "🔍 Health check: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/health-check/"
echo "📊 API endpoints:"
echo "   - GET /inventory/transactions"
echo "   - POST /inventory/transactions/create"
echo "   - GET /inventory/summary"
echo "   - GET /products"
