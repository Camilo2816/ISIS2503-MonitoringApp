-- Script de configuración de base de datos PostgreSQL para el sistema de inventario
-- Ejecutar en Amazon RDS PostgreSQL

-- Crear base de datos
CREATE DATABASE inventory_db;

-- Crear usuario para la aplicación
CREATE USER inventory_user WITH PASSWORD 'inventory_password_2024';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;

-- Conectar a la base de datos
\c inventory_db;

-- Otorgar permisos en el esquema público
GRANT ALL ON SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO inventory_user;

-- Configurar permisos por defecto para futuras tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inventory_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO inventory_user;

-- Configuraciones específicas para RDS
-- Habilitar extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Configurar parámetros de rendimiento para el experimento
-- (Estos se configuran en el parámetro group de RDS)
-- shared_preload_libraries = 'pg_stat_statements'
-- track_activity_query_size = 2048
-- pg_stat_statements.max = 10000
-- pg_stat_statements.track = 'all'

COMMENT ON DATABASE inventory_db IS 'Base de datos para el sistema de inventario de bodega - Experimento ALB + EC2 + RDS';
