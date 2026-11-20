# 0003 — Servidor A, contenedor propio, no crítico

- **Estado:** Aceptada (decisión del usuario)
- **Fecha:** 2026-11-19

## Contexto
B (producción del ERP) tiene disco de 29 GB que ya llegó al 93 % (2026-10-19). A es el servidor de
respaldo y failover del ERP: recibe los respaldos diarios de `erp_db`, tiene el ERP instalado pero
apagado (`ERP_RESTART_POLICY=no`), Keycloak y nginx-proxy-manager.

## Decisión
- Frappe Learning vive en A, en su propio `docker-compose` y carpeta, con `restart: unless-stopped`.
- Se publica por un subdominio dado de alta en nginx-proxy-manager de A (no por el túnel de B).
- Es un servicio **no crítico**: si se cae, la intranet sigue funcionando.

## Consecuencias
- Hay que revisar disco y RAM de A antes de instalar (P4).
- En un failover del ERP hacia A, ambos corren a la vez: Frappe lleva límites de memoria.
- Su mantenimiento no requiere ventana del ERP, pero sí autorización de la persona y aviso si hay gente
  tomando cursos.
