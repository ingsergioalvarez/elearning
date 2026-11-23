# Changelog — Comunicalo Learning

Historial de cambios significativos. Entrada nueva arriba de todo, con fecha real.

---

## 2026-11-23 — Login con número de empleado y contraseña del ERP instalado en A (comunicalo_auth 0.1.0)

- App propia `apps/comunicalo_auth` instalada en el sitio. Reemplaza `/login` sin tocar Frappe ni lms (la
  página `www/login` de la última app instalada tiene prioridad) y abre la sesión con `LoginManager.login_as`.
- `Administrator` sigue entrando en la misma pantalla con su contraseña local (no pasa por el ERP).
- Campos nuevos en User: `numero_empleado`, `empresa_erp`, `area_erp`. Registro libre desactivado.
- Aprendido a la mala (en el código): lms reemplaza los `username` de menos de 4 caracteres; por eso la
  identidad es el campo `numero_empleado` y los números cortos usan `emp<número>` como username.
- Frappe solo guarda variables locales en las trazas con `developer_mode`: **nunca activarlo en A**.
- Imagen en dos capas: base (Frappe+lms+payments, sin cambios) + `...-auth0.1.0` con la app; el script
  corre las 27 pruebas unitarias dentro de la imagen. Respaldo previo: `20261123_094315-...` en el sitio.
- Verificado sin cuentas reales: `/login` nuevo, datos vacíos, número inexistente → «Credenciales
  inválidas» del ERP, y correos a `.local` se omiten (prueba con rollback). Falta el camino feliz
  (Sergio Alberto en el navegador) y los errores con el empleado de prueba de RH (decisión 0010).
- ERP: se entregó el prompt para el botón «Cursos» con la opción B (permiso solo para Desarrollo).
- Acceso de visitantes desactivado (`allow_guest_access = 0`): tras cerrar sesión, volver desde el ERP
  mostraba el catálogo como visitante. El enlace del ERP pasa a ser `/login?redirect-to=/lms`.
- Learning valida siempre contra el ERP de **producción** (`erp_api_url`), aunque el botón se pruebe desde
  un ERP local: los usuarios se crean solos en su primer login, no hay migración de usuarios.

## 2026-11-23 — Definiciones del login contra el ERP (P6, P7, roles, pruebas)

- **P6:** `ERP_API_URL=https://grupocomunicalo.mx` (sin `/api`). `/intranet` es la página de React, no la
  API. POST vacío a `/api/auth/login` → 400, verificado desde desarrollo, desde A y desde dentro del
  contenedor de Learning (Cloudflare no bloquea al servidor).
- **Decisión 0010:** el login se prueba primero con respuestas simuladas del ERP; luego contra producción:
  camino feliz con la cuenta de Sergio Alberto en el navegador, errores con un empleado de prueba de RH
  (fuera de nómina, se inactiva al terminar). Nunca contraseñas por chat, comandos, logs o archivos.
- **Decisión 0011 (P7 y roles):** identidad por `username = numero_empleado`; correo técnico
  `<numero>@empleados.grupocomunicalo.local` si no hay corporativo; `rename_doc` si cambia el correo; sin
  correos a `.local`. Roles en dos etapas: hoy todos estudiantes y administradores a mano; cuando el ERP
  tenga `CURSOS_VER`/`CURSOS_ADMINISTRAR`, primero se migran los administradores al ERP y luego se activa
  la sincronización.
- Se ajustó el paso 4 de `CLAUDE.md` y el estado de la decisión 0005 (su punto 4 lo precisa 0011).

## 2026-11-20 — Learning instalado en A (Fase 0 en A, sin entorno local)

- **Decisión 0009:** no se usa Docker local; las pruebas se hacen en A. Se ajustó el paso 4 de `CLAUDE.md`.
- Versiones instaladas: Frappe **v16.60.2**, lms **v16.3.0**, payments **v16.0.1** (commit `1978965f38b8`),
  frappe_docker **v4.2.0** (la v4.3.0 salió el mismo día; se evalúa después), Python 3.14.10,
  MariaDB 11.8.9, Redis 8.6.8-alpine. Imagen `comunicalo/learning:f16.60.2-lms16.3.0-pay16.0.1`.
- Se usa `images/custom/Containerfile`, no `layered`: Docker Hub no publica `frappe/build` con la etiqueta
  exacta de Frappe, así que `layered` no permite fijar la versión.
- Sitio `elearning.grupocomunicalo.mx` en `/opt/apps/learning`, proyecto `learning`, solo en
  `127.0.0.1:8090` y unido a `proxy_net` de nginx-proxy-manager. Registro DNS creado en Cloudflare.
- La construcción tardó unos 15 min y dejó como mínimo 2.9 GB de RAM libre; generó 21 GB de caché, que se
  limpió con `docker builder prune` (no toca imágenes, contenedores ni volúmenes). En reposo Learning usa ~0.8 GB.
- Se creó swap de 4 GB en A (`/swapfile`, `swappiness=10`): sin swap, un failover con todo encendido podía
  hacer que Linux matara procesos (incluido MySQL del ERP). Copia previa: `/etc/fstab.respaldo-2026-11-20`.
- Keycloak en A **no está dormido**: corre (~520 MB, `restart: always`) y, según el usuario, lo usa otra
  app del ERP. Learning no lo usa ni lo toca (0006 sigue vigente).
- Hallazgo para P11 (código de `lms` v16.3.0): el reproductor SCORM solo guarda completado y `suspend_data`;
  no guarda calificación, y en SCORM 1.2 solo marca completo con `passed` (no con `completed`). Falta probarlo.
- Remoto: `github.com/ingsergioalvarez/elearning`.

## 2026-11-19 — Conexión a A, plantilla .env y skill de despliegue

- `CLAUDE.local.md` (fuera de git): comando SSH a A y carpetas del ERP que no se tocan.
- `infra/.env.example`: variables de Learning (versiones fijas, sitio, MariaDB propia, `ERP_API_URL`,
  límites de memoria). El `.env` del ERP no se copia: Frappe no usa sus secretos.
- Skill `desplegar-learning`: respaldo verificado, actualización y reinicio solo de `-p learning`,
  verificación y registro.
- Riesgo detectado: en A, el ERP está detenido como failover. `docker container prune` o
  `docker system prune` borrarían sus contenedores. Quedó prohibido en `CLAUDE.md` y en la skill.
- Nueva pregunta P12: repositorio remoto y cómo llega el código a A.

## 2026-11-19 — Resueltas P2 y P3: no hay cursos previos; Frappe v16

- **P2:** no existen cursos; se diseñarán desde cero. La Fase 0 se prueba con un curso de muestra y un
  paquete SCORM de muestra.
- **P3 / decisión 0008:** Frappe v16 + Learning y payments en `version-16`, con etiquetas fijas.
  El 2026-11-04 Learning dejó la numeración v2.x (`main`) y ahora sigue la versión del framework;
  `version-15` quedó congelada.
- Nueva pregunta P11: con qué se hará el contenido interactivo. Se decide después de probar SCORM.

## 2026-11-19 — Confirmadas P1 y P8

- **P1 / decisión 0001 aceptada:** el módulo E-learning del ERP se queda como repositorio de documentos;
  Frappe Learning es solo para cursos y capacitaciones.
- **P8 / decisión 0004 aceptada completa:** respaldo local diario en A con 7 días de retención, sin copia a B.
- Siguen abiertas para la Fase 0: P2 (formato de los cursos) y P3 (versión de Frappe/lms a fijar).

## 2026-11-19 — Creación del proyecto y decisiones iniciales

- Se crea el repositorio aparte del ERP para montar Frappe Learning como plataforma de cursos.
- Decisiones registradas en `docs/decisiones/` (0001 a 0007):
  - Frappe Learning para **cursos**; el módulo E-learning del ERP se queda como repositorio de
    **documentos** (propuesta, por confirmar con el usuario).
  - Proyecto y repositorio aparte; en el ERP solo un enlace «Cursos».
  - Servidor A, contenedor propio, no crítico.
  - Sin respaldo hacia B; se propone respaldo local diario en A.
  - Login propio en Frappe que valida número de empleado y contraseña contra `POST /api/auth/login`
    del ERP (misma contraseña). SSO de un clic queda como opción futura.
  - No se usa el Keycloak que corre en A.
- Contrato con el ERP documentado en `docs/contexto-erp.md` (revisado contra el código del ERP ese día).
- Estado: Fase 0 sin iniciar. Aún no hay nada instalado ni en local ni en A.
