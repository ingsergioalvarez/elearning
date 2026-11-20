# Plan de trabajo

Se actualiza al cerrar cada sesión: marcar casillas, mover preguntas resueltas a una decisión o al
CHANGELOG. **Fase actual: 0 (sin iniciar).**

---

## Preguntas abiertas (resolver con la persona antes de la fase que las necesita)

| # | Pregunta | Se necesita en |
|---|---|---|
| ~~P1~~ | **Resuelta 2026-11-19:** documentos se quedan en E-learning del ERP; Frappe solo para cursos (decisión 0001 aceptada) | Fase 0 |
| ~~P2~~ | **Resuelta 2026-11-19:** no hay cursos todavía; se diseñarán desde cero. Las pruebas de la Fase 0 se hacen con un curso de muestra | Fase 0 |
| ~~P3~~ | **Resuelta 2026-11-19:** Frappe v16 + Learning version-16 con etiquetas fijas (decisión 0008) | Fase 0 |
| P12 | ¿Repositorio remoto (GitHub privado)? Define cómo llega el código a A: `git pull` con llave de despliegue de solo lectura, o `scp` del commit revisado mientras no haya remoto | Fase 1 |
| P11 | ¿Con qué se hará el contenido interactivo de los cursos? Opciones: el editor de Frappe solo; una herramienta de autor que exporte SCORM (comercial o gratuita); o actividades HTML propias empaquetadas como SCORM. Se decide después de probar SCORM en la Fase 0 | Fase 4 |
| P4 | ¿Disco, RAM y puertos libres en A? (revisión de solo lectura: `df -h`, `free -h`, `docker ps`) | Fase 1 |
| P5 | ¿Nombre del subdominio? (propuesta: `cursos.grupocomunicalo.mx`) | Fase 1 |
| P6 | ¿URL pública de la API del ERP que usará Frappe para validar el login? | Fase 2 |
| P7 | ¿Qué hacer con empleados sin `correo_corporativo`? (propuesta: correo técnico `<numero>@empleados.grupocomunicalo.local` que nunca recibe correos) | Fase 2 |
| ~~P8~~ | **Resuelta 2026-11-19:** respaldo local diario en A con 7 días de retención (decisión 0004 aceptada) | Fase 1 |
| P9 | ¿Quién administra cursos (personas de RH, Calidad)? Para asignar `CURSOS_ADMINISTRAR` | Fase 4 |
| P10 | ¿Videos dentro de Frappe o en YouTube no listado / Vimeo incrustado? (afecta el disco de A) | Fase 4 |

---

## Fase 0 — Prueba en local (solo la máquina de desarrollo)

- [x] Resolver P1 (2026-11-19).
- [x] Resolver P2 y P3 (2026-11-19).
- [ ] `infra/docker-compose.yml` local basado en `frappe_docker`, con Frappe v16, `lms` y `payments`
      version-16 y etiquetas o commits exactos (decisión 0008). Anotar las versiones en el CHANGELOG.
- [ ] Sitio local creado, idioma `es-MX`, zona horaria `America/Mexico_City`.
- [ ] Armar **un curso de muestra** con todo lo que da Frappe: texto, video, PDF o presentación,
      cuestionario, tarea con entrega, certificado e insignia. Revisar el avance por persona.
- [ ] Probar un **paquete SCORM de muestra**: que cargue, que marque completado y si guarda o no la
      calificación y el avance (pausa y reanuda). Con esto se resuelve P11.
- [ ] Probar cómo se ve en celular.
- [ ] **Decisión de ir o no ir:** ¿cubre lo que se necesita? Registrar el resultado en el CHANGELOG.

## Fase 1 — Servidor A (requiere autorización de la persona para cada paso que cambie A)

- [x] Resolver P8 (2026-11-19).
- [ ] Resolver P4, P5, P12.
- [ ] `.env` real creado en A (desde `infra/.env.example`) y copia en el gestor de contraseñas.
- [ ] Confirmar en `CLAUDE.local.md` y en la skill `desplegar-learning` los comandos reales
      (carpeta, `-p learning`, servicio, sitio).
- [ ] Revisar que el build de la imagen quepa en la RAM de A. Si no, construir en local y llevar la imagen.
- [ ] Carpeta propia en A (propuesta: `/opt/apps/learning`), separada de la del ERP.
- [ ] `docker-compose` propio con `restart: unless-stopped`, rotación de logs (`json-file`, 20m × 3) y
      límites de memoria que dejen espacio al ERP en caso de failover.
- [ ] Subdominio en Cloudflare y en nginx-proxy-manager de A, con HTTPS.
- [ ] `scripts/respaldo_local.sh` + cron (`bash <script>`), con 7 días de retención y aviso si falla.
- [ ] Probar una restauración en local con un respaldo real (si no se probó, no hay respaldo).
- [ ] `docs/runbook-servidor-a.md` completo.

## Fase 2 — Misma contraseña que el ERP (app `apps/comunicalo_auth`)

- [ ] Resolver P6, P7.
- [ ] Elegir el mecanismo de Frappe para reemplazar el login **sin modificar el core** (ver `apps/README.md`).
- [ ] Pantalla de login con «Número de empleado» y «Contraseña».
- [ ] Validación contra `POST /api/auth/login`, perfil con `GET /api/rh/mi-perfil`.
- [ ] Alta o actualización automática del usuario de Frappe (nombre, correo, empresa y área).
- [ ] Roles de Frappe según `CURSOS_VER` / `CURSOS_ADMINISTRAR`, sincronizados en cada login.
- [ ] Manejo de errores: inválido, bloqueado, inactivo, ERP caído, ERP en mantenimiento (perfil 503).
- [ ] La contraseña no aparece en logs ni en errores (revisar).
- [ ] Cuenta `Administrator` local de Frappe solo para emergencias, con contraseña guardada por Desarrollo.
- [ ] Pruebas contra el **ERP local** con usuarios de prueba.
- [ ] Pedir en el ERP los pendientes 1 de `docs/pendientes-erp.md`.

## Fase 3 — Enlace desde la intranet (se hace en el repo del ERP)

- [ ] Pendientes 2, 3 y 4 de `docs/pendientes-erp.md`.

## Fase 4 — Contenido y piloto

- [ ] Resolver P9, P10 y P11.
- [ ] Marca: logo y colores azul/gris desde la configuración de Frappe.
- [ ] Diseñar los 2–3 primeros cursos y abrirlos a un área piloto.
- [ ] Ajustes con lo que reporte el piloto. Abrir a todos.

## Fase 5 — Opcional

- [ ] Avance y certificados visibles en el ERP (pendiente 7).
- [ ] Avisos de cursos pendientes en la campana del ERP.
- [ ] Entrar con un clic, sin contraseña (pendiente 6, reemplaza parte de la decisión 0005).
