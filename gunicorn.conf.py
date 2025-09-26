# Configuración de Gunicorn para el experimento ALB + EC2
import multiprocessing

# Configuración del servidor
bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configuración de procesos
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración para ALB health checks
def when_ready(server):
    server.log.info("Servidor Gunicorn iniciado en puerto 8080")

def worker_int(worker):
    worker.log.info("Worker recibió SIGINT o SIGQUIT")

def pre_fork(server, worker):
    server.log.info("Worker %s iniciado", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker %s (pid: %s) iniciado", worker.age, worker.pid)
