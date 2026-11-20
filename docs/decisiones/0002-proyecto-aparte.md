# 0002 — Proyecto y repositorio aparte del ERP

- **Estado:** Aceptada (decisión del usuario)
- **Fecha:** 2026-11-19

## Contexto
Frappe es otro stack (Python, MariaDB, Redis, procesos en segundo plano) con su propio ciclo de
actualizaciones. En el ERP, todo lo que llega a `main` aparece en Mantenimiento del sistema y se publica
con el siguiente deploy, que reinicia todo el ERP.

## Decisión
- Repositorio propio: `comunicalo-learning` (carpeta hermana de `grupocomunicalo`).
- En el ERP solo se hacen cambios mínimos de integración (enlace «Cursos», permisos), desde el repo del
  ERP y con su flujo. Se listan en `docs/pendientes-erp.md`.

## Consecuencias
- Los cambios de Frappe no ensucian la lista de cambios del ERP ni lo reinician.
- El agente de este repo no edita el ERP; el contexto necesario está en `docs/contexto-erp.md`.
- Hay dos CHANGELOG: cada uno registra lo suyo.
