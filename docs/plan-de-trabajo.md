# Plan de trabajo

Se actualiza al cerrar cada sesión: marcar casillas, mover preguntas resueltas a una decisión o al
CHANGELOG. **Fase actual: 0, en A (decisión 0009).** Learning instalado en A el 2026-11-20.

---

## Preguntas abiertas (resolver con la persona antes de la fase que las necesita)

| # | Pregunta | Se necesita en |
|---|---|---|
| ~~P1~~ | **Resuelta 2026-11-19:** documentos se quedan en E-learning del ERP; Frappe solo para cursos (decisión 0001 aceptada) | Fase 0 |
| ~~P2~~ | **Resuelta 2026-11-19:** no hay cursos todavía; se diseñarán desde cero. Las pruebas de la Fase 0 se hacen con un curso de muestra | Fase 0 |
| ~~P3~~ | **Resuelta 2026-11-19:** Frappe v16 + Learning version-16 con etiquetas fijas (decisión 0008) | Fase 0 |
| P12 | **Parcial 2026-11-20:** remoto `github.com/ingsergioalvarez/elearning` (privado). Falta cómo baja a A: llave de despliegue de solo lectura (hoy se copia con `scp`) | Fase 1 |
| P11 | ¿Con qué se hará el contenido interactivo de los cursos? Opciones: el editor de Frappe solo; una herramienta de autor que exporte SCORM (comercial o gratuita); o actividades HTML propias empaquetadas como SCORM. Se decide después de probar SCORM en la Fase 0 | Fase 4 |
| ~~P4~~ | **Resuelta 2026-11-20:** 2 núcleos, 7.8 GB RAM + 4 GB swap nuevo, 96 GB disco (27 % usado). 8080 lo usa Keycloak; Learning usa 127.0.0.1:8090 | Fase 1 |
| ~~P5~~ | **Resuelta 2026-11-20:** `elearning.grupocomunicalo.mx` (registro creado en Cloudflare) | Fase 1 |
| ~~P6~~ | **Resuelta 2026-11-23:** `ERP_API_URL=https://grupocomunicalo.mx` (sin `/api`), verificada desde A (`docs/contexto-erp.md`) | Fase 2 |
| ~~P7~~ | **Resuelta 2026-11-23:** correo técnico `<numero>@empleados.grupocomunicalo.local`; identidad por `numero_empleado` y renombrado si cambia el correo (decisión 0011) | Fase 2 |
| ~~P8~~ | **Resuelta 2026-11-19:** respaldo local diario en A con 7 días de retención (decisión 0004 aceptada) | Fase 1 |
| P9 | ¿Quién administra cursos (personas de RH, Calidad)? Por ahora se asignan a mano en Learning (decisión 0011, etapa 1); faltan los nombres | Fase 4 |
| P10 | ¿Videos dentro de Frappe o en YouTube no listado / Vimeo incrustado? (afecta el disco de A) | Fase 4 |

---

## Fase 0 — Prueba en local (solo la máquina de desarrollo)

- [x] Resolver P1 (2026-11-19).
- [x] Resolver P2 y P3 (2026-11-19).
- [x] `infra/docker-compose.yml` basado en `frappe_docker` v4.2.0, Frappe v16.60.2, lms v16.3.0, payments
      v16.0.1 (2026-11-20). Se hace en A, no en local (decisión 0009).
- [x] Sitio `elearning.grupocomunicalo.mx` creado en A con payments y lms (2026-11-20).
- [ ] Entrada en nginx-proxy-manager con HTTPS y websockets → `learning-frontend-1:8080`.
- [ ] Asistente inicial: idioma `es-MX` (o `es` si no existe), zona horaria `America/Mexico_City`.
- [ ] Guardar `ADMIN_PASSWORD` y `DB_ROOT_PASSWORD` del `.env` de A en el gestor de contraseñas.
- [ ] Armar **un curso de muestra** con todo lo que da Frappe: texto, video, PDF o presentación,
      cuestionario, tarea con entrega, certificado e insignia. Revisar el avance por persona.
- [ ] Probar un **paquete SCORM de muestra**: que cargue, que marque completado y si guarda o no la
      calificación y el avance (pausa y reanuda). Con esto se resuelve P11.
- [ ] Probar cómo se ve en celular.
- [ ] **Decisión de ir o no ir:** ¿cubre lo que se necesita? Registrar el resultado en el CHANGELOG.

## Fase 1 — Servidor A (requiere autorización de la persona para cada paso que cambie A)

- [x] Resolver P8 (2026-11-19).
- [x] Resolver P4 y P5 (2026-11-20). - [ ] P12: llave de despliegue.
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

- [x] Resolver P6 y P7 (2026-11-23; decisiones 0010 y 0011).
- [x] Mecanismo sin modificar el core: página `www/login` propia (las apps instaladas después tienen
      prioridad) + método `comunicalo_auth.login.entrar` + `LoginManager.login_as` (2026-11-23).
- [x] Pantalla de login con «Número de empleado» y «Contraseña» (2026-11-23).
- [x] Validación contra `POST {ERP_API_URL}/api/auth/login`, perfil con `GET {ERP_API_URL}/api/rh/mi-perfil` (2026-11-23).
- [x] Usuario identificado por el campo `numero_empleado` (username = número, o `emp<número>` si tiene menos de
      4 caracteres porque lms los reemplaza); correo corporativo o técnico `.local`; renombrado si cambia el correo.
- [x] Sin correo de bienvenida; destinatarios `.local` se quitan de la cola (probado 2026-11-23).
- [x] Roles etapa 1: asegura `LMS Student`; nunca quita roles de administrador (decisión 0011).
- [x] Manejo de errores: inválido, bloqueado, inactivo, ERP caído, ERP en mantenimiento (perfil 503), timeout.
- [x] La contraseña y el token no se guardan ni se registran (revisado; `developer_mode` apagado en A).
- [x] Registro libre de usuarios desactivado (solo entran empleados validados por el ERP).
- [x] Cuenta `Administrator` local de Frappe solo para emergencias, con contraseña guardada por Desarrollo (KeePassXC, 2026-11-20).
- [x] Pruebas unitarias con respuestas simuladas del ERP: 27 pruebas, 200/400/401/403/405/500, perfil 503/404, timeout (2026-11-23).
- [x] Prueba sin cuenta real: número inexistente → el ERP responde «Credenciales inválidas» y se muestra (2026-11-23).
- [ ] Camino feliz validado por Sergio Alberto con su cuenta, en el navegador.
- [ ] RH da de alta un **empleado de prueba** (fuera de nómina y reportes) para probar contraseña mala y
      bloqueo; al terminar, RH lo inactiva.
- [ ] Etapa 2 de roles (cuando el ERP tenga el pendiente 1): migrar administradores manuales al ERP y
      después activar la sincronización.

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
