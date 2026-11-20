---
name: desplegar-learning
description: Despliega Comunicalo Learning (Frappe Learning) en el servidor A por SSH. Antes de actualizar hace un respaldo verificado y después revisa que el sitio siga funcionando. Usar cuando la persona pida "despliega Learning", "sube la app al servidor A", "actualiza Frappe en A" o "instala Learning en A". Invocar esta skill es la autorización de la persona para conectarse a A y reconstruir SOLO los contenedores de Learning. No autoriza tocar nada del ERP.
---

# Desplegar Comunicalo Learning en el servidor A

> **Estado:** procedimiento base. Los comandos exactos (nombre del proyecto de compose, servicio
> `backend`, nombre del sitio) se confirman en la Fase 0/1 y se actualizan aquí y en
> `docs/runbook-servidor-a.md`. Si un comando de aquí no coincide con lo instalado, **detente y pregunta**.

## Autorización

Invocar esta skill autoriza, en ese momento:
- conectarse por SSH a A con el comando de `CLAUDE.local.md`;
- respaldar el sitio, actualizar el código de `/opt/apps/learning`, reconstruir y reiniciar **solo** los
  contenedores del proyecto de compose de Learning, y correr `bench migrate`.

**No autoriza:** tocar `/opt/apps/erpmodular`, los contenedores `erpmod_*`, Keycloak, el cron o los
respaldos del ERP, ni saltar a B. Si algo de eso parece necesario, detente y pregunta.

## Antes de empezar (pausa real si no se cumple)

1. El cambio está **probado en local** y commiteado en `main` de este repo (y subido al remoto, si existe).
2. La persona sabe que Learning estará fuera de 2 a 10 minutos. No necesita ventana del ERP, porque no lo
   afecta, pero si es horario de trabajo y hay gente tomando cursos, pregunta si conviene esperar.
3. `CLAUDE.local.md` existe y tiene el comando SSH. Si no existe, no improvises la conexión: pregunta.

## Pasos

### 1. Revisar A (solo lectura)
```bash
df -h /            # si el disco pasa del 85 %, detente y avisa
free -h
docker ps --format '{{.Names}}\t{{.Status}}'
```
Confirma que los contenedores `erpmod_*` siguen **detenidos** y que no los vas a tocar.

### 2. Respaldo verificado (obligatorio)
```bash
cd /opt/apps/learning/infra
docker compose -p learning exec backend bench --site "$SITE_NAME" backup --with-files
docker compose -p learning exec backend ls -lh sites/"$SITE_NAME"/private/backups | tail -5
```
Si el respaldo falla o no aparece el archivo de hoy, **no sigas**.

### 3. Actualizar el código al commit revisado
```bash
cd /opt/apps/learning
git fetch origin && git reset --hard <commit-revisado>
```
(Si todavía no hay remoto, el código llega por `scp` del commit revisado. Anota cómo se hizo.)

### 4. Construir y reiniciar SOLO Learning
```bash
cd /opt/apps/learning/infra
docker compose -p learning build          # imagen con versiones fijas del .env
docker compose -p learning up -d
docker compose -p learning exec backend bench --site "$SITE_NAME" migrate
docker image prune -f                     # solo imágenes sin etiqueta; nada más
```

### 5. Verificar
- `docker compose -p learning ps`: todo `Up`.
- `curl -sI https://<subdominio>` responde 200 o 302.
- Iniciar sesión con un usuario de prueba (número de empleado y contraseña del ERP) y abrir un curso.
- `docker compose -p learning logs --tail 100 backend`: sin errores nuevos.
- Los contenedores `erpmod_*` siguen igual que en el paso 1.

### 6. Registrar
- CHANGELOG: fecha, commit desplegado y versiones (Frappe / lms / payments) si cambiaron.
- `docs/runbook-servidor-a.md`: cualquier comando que haya cambiado.
- Informa a la persona: qué se desplegó, el resultado de la verificación y dónde quedó el respaldo.

## Si algo sale mal
- Falla el build: los contenedores anteriores siguen corriendo; no hagas `down`. Informa.
- Falla `migrate` o el sitio no abre: **no restaures por tu cuenta**. Informa y propone restaurar el
  respaldo del paso 2 (`bench --site ... restore`, con los archivos), con la autorización de la persona.

## Prohibido en A, siempre
- `docker compose down -v`, `docker volume rm`, `docker volume prune`.
- `docker container prune`, `docker system prune` (con o sin `-a`): **borrarían los contenedores
  detenidos del ERP**, que son el failover.
- `bench drop-site`, `bench --force reinstall`, `bench restore` sin autorización explícita.
- Cualquier `docker compose` sin `-p learning` o fuera de `/opt/apps/learning`.
- Editar archivos fuera de `/opt/apps/learning`.
