# Runbook — Comunicalo Learning en el servidor A

> **Estado: por llenar en la Fase 1.** Nada de esto existe aún en A. Cada sección se completa con los
> comandos reales en cuanto se ejecutan por primera vez (y se prueban).

Reglas que aplican siempre: ver «Producción (servidor A)» en `CLAUDE.md`. Nada del ERP en A se toca.

- **Conexión:** comando en `CLAUDE.local.md` (privado, fuera de git).
- **Despliegue y actualización:** skill `.claude/skills/desplegar-learning/SKILL.md`. Este runbook es la
  referencia de los comandos; la skill es el procedimiento paso a paso. Si cambia uno, se actualiza el otro.
- **Variables:** plantilla en `infra/.env.example`; el `.env` real vive solo en A y en el gestor de contraseñas.

## Ubicación
- Carpeta: _(propuesta `/opt/apps/learning`)_
- Proyecto de compose: _(nombre)_
- Contenedores: _(lista)_
- Volúmenes: _(lista, cuál guarda la base, cuál los archivos)_
- Subdominio y entrada en nginx-proxy-manager: _(…)_

## Levantar / detener
_(comandos; nunca `down -v`)_

## Ver logs y estado
_(comandos)_

## Respaldo local
- Script: `scripts/respaldo_local.sh`, cron: _(línea exacta, con `bash`)_
- Dónde quedan y retención: _(…)_
- Cómo verificar que corrió: _(…)_

## Restaurar
_(pasos probados en local)_

## Actualizar Frappe / lms
1. `bench backup --with-files` y verificar el archivo.
2. _(cambiar versión fija en compose, pull/build, migrate)_
3. _(verificación posterior)_
4. Anotar versión nueva en CHANGELOG.

## Si el ERP hace failover a A
_(qué revisar: memoria, que ambos sigan arriba)_

## Qué NO hacer
- `docker compose down -v`, `docker volume rm`, `bench drop-site`, `bench --force reinstall`.
- Tocar el compose, `.env` o respaldos del ERP, o el Keycloak.
