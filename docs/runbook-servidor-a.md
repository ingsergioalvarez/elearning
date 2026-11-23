# Runbook — Comunicalo Learning en el servidor A

> **Estado:** instalado en A el 2026-11-20 (decisión 0009: no hay entorno local). Faltan respaldo,
> restauración probada y actualización; se completan cuando se ejecuten por primera vez.

Reglas que aplican siempre: ver «Producción (servidor A)» en `CLAUDE.md`. Nada del ERP en A se toca.

- **Conexión:** comando en `CLAUDE.local.md` (privado, fuera de git).
- **Despliegue y actualización:** skill `.claude/skills/desplegar-learning/SKILL.md`. Este runbook es la
  referencia de los comandos; la skill es el procedimiento paso a paso. Si cambia uno, se actualiza el otro.
- **Variables:** plantilla en `infra/.env.example`; el `.env` real vive solo en A y en el gestor de contraseñas.

## Ubicación
- Carpeta: `/opt/apps/learning` (`infra/` con compose y `.env`, `scripts/`, `build/` con el clon de
  frappe_docker y el log de construcción).
- Proyecto de compose: `learning` (fijo en el compose con `name:`; aun así usar siempre `-p learning`).
- Contenedores: `learning-{backend,frontend,websocket,queue-short,queue-long,scheduler,db,redis-cache,redis-queue}-1`
  y `learning-configurator-1` (termina al arrancar, es normal que esté `Exited (0)`).
- Volúmenes: `learning_db-data` (base MariaDB), `learning_sites` (configuración del sitio y **archivos
  subidos**: SCORM, PDF, videos), `learning_redis-queue-data` (cola).
- Sitio: `elearning.grupocomunicalo.mx`. Escucha en `127.0.0.1:8090` de A y el frontend está unido a la
  red `proxy_net` de nginx-proxy-manager, que reenvía a `learning-frontend-1:8080`.
- DNS: registro A `elearning` en Cloudflare (proxy activo; SSL en modo Full).
- Imagen en dos capas (`bash scripts/construir_imagen.sh`, lee `infra/.env`):
  - `IMAGEN_BASE=comunicalo/learning:f16.60.2-lms16.3.0-pay16.0.1`: Frappe + payments + lms (unos 15 min;
    se omite si ya existe).
  - `IMAGEN_LEARNING=comunicalo/learning:f16.60.2-lms16.3.0-pay16.0.1-auth0.1.0`: base + `apps/comunicalo_auth`
    (segundos). El script corre al final las pruebas unitarias de la app dentro de la imagen.
  - Al cambiar el código de `apps/`, subir la versión en `IMAGEN_LEARNING` (nunca reusar una etiqueta).
- Apps del sitio: frappe, payments, lms, comunicalo_auth (login con número de empleado y contraseña del ERP).
- Configuración del login en el site_config (no en código):
  `bench --site elearning.grupocomunicalo.mx set-config erp_api_url https://grupocomunicalo.mx` y
  `set-config -p erp_timeout_segundos 10`.
- Learning sin acceso de visitantes: `LMS Settings.allow_guest_access = 0` (2026-11-23). Sin sesión, `/lms` manda a `/login`.
- Enlace desde el ERP: `https://elearning.grupocomunicalo.mx/login?redirect-to=/lms`.
- **Nunca activar `developer_mode` en A:** con él, las trazas de error guardan variables locales
  (podrían incluir la contraseña de un login fallido).
- Swap del servidor: `/swapfile` 4 GB, `vm.swappiness=10` (`/etc/sysctl.d/99-swap-learning.conf`).
  Respaldo de fstab previo: `/etc/fstab.respaldo-2026-11-20`.

## Levantar / detener
```bash
cd /opt/apps/learning/infra
docker compose -p learning up -d
docker compose -p learning stop        # detener sin borrar nada. Nunca `down -v`.
```

## Ver logs y estado
```bash
cd /opt/apps/learning/infra
docker compose -p learning ps -a
docker compose -p learning logs --tail 100 backend
curl -s http://127.0.0.1:8090/api/method/ping      # {"message":"pong"}
docker stats --no-stream | grep learning
```

## Respaldo local
- Script: `scripts/respaldo_local.sh`, cron: _(línea exacta, con `bash`)_
- Dónde quedan y retención: _(…)_
- Cómo verificar que corrió: _(…)_

## Restaurar
_(pasos probados en local)_

## Actualizar Frappe / lms / apps propias
Probado el 2026-11-23 al instalar `comunicalo_auth`:
1. Respaldo verificado:
   `docker compose -p learning exec -T backend bench --site elearning.grupocomunicalo.mx backup --with-files`
   y `ls -lh sites/<sitio>/private/backups/` dentro del contenedor (que aparezcan los archivos de hoy).
2. Copiar el código revisado a `/opt/apps/learning` (hoy con `tar` por SSH; con llave de despliegue en P12).
3. Copia del `.env` (`cp -p .env .env.respaldo-AAAA-MM-DD`) y cambiar solo las etiquetas de versión.
4. `bash scripts/construir_imagen.sh` (si cambia Frappe/lms/payments, cambiar también `IMAGEN_BASE`).
5. `docker compose -p learning up -d` (recrea solo Learning; fuera menos de un minuto).
6. `bench --site <sitio> migrate` (o `install-app` si la app es nueva).
7. Verificar: `/login`, `/api/method/ping`, `docker compose -p learning ps`, Error Log vacío.
8. Anotar versiones en el CHANGELOG.

## Si el ERP hace failover a A
_(qué revisar: memoria, que ambos sigan arriba)_

## Qué NO hacer
- `docker compose down -v`, `docker volume rm`, `bench drop-site`, `bench --force reinstall`.
- Tocar el compose, `.env` o respaldos del ERP, o el Keycloak.
