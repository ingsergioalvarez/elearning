# Contexto del ERP para este proyecto

Lo que Comunicalo Learning necesita saber del ERP. Revisado contra el código del ERP el **2026-11-19**.
Si algo aquí no coincide con el ERP actual, gana el código del ERP: se corrige este archivo y se anota en
el CHANGELOG.

- **Repositorio del ERP:** `../grupocomunicalo` (Node.js + Express, React, MySQL `erp_db`). Sus reglas:
  `../grupocomunicalo/CLAUDE.md`. Desde aquí solo se **lee**; los cambios se hacen allá (`docs/pendientes-erp.md`).
- **URL pública de la API del ERP:** _pendiente de confirmar_ (ver preguntas abiertas en el plan).
  Va en `.env` como `ERP_API_URL`, nunca en código.

---

## 1. Login: `POST {ERP_API_URL}/api/auth/login`

Público (sin token). Código: `backend/src/modules/auth/auth.controller.js` y `auth.service.js`.

**Petición**
```json
{ "numero_empleado": "1234", "password": "********" }
```
- El ERP quita **todos** los espacios de ambos campos y pasa `numero_empleado` a MAYÚSCULAS.
- `numero_empleado` máximo 30 caracteres; `password` máximo 72 (si es más larga responde 401).
- **El usuario entra con número de empleado, no con correo.** La pantalla de login de Frappe debe pedir
  «Número de empleado».

**Respuesta exitosa (200)**
```json
{
  "success": true,
  "message": "Inicio de sesión exitoso",
  "data": {
    "token": "<JWT, expira en 24h por omisión>",
    "empleado": {
      "id": 15,
      "numero_empleado": "1234",
      "nombre_completo": "Nombre Apellido Apellido",
      "roles": ["..."],
      "permisos": ["ELEARNING_VER", "..."],
      "grupos": ["..."]
    }
  }
}
```
- **No trae correo ni empresa.** Para eso se usa el perfil (sección 2).

**Errores**
| Código | Cuándo | Qué mostrar en Frappe |
|---|---|---|
| 400 | Faltan campos o número demasiado largo | El `message` del ERP |
| 401 | Credenciales inválidas («Intentos restantes: N»), cuenta inactiva | El `message` del ERP |
| 403 | Cuenta bloqueada (3 intentos fallidos) | El `message` + «Desbloquéala desde la intranet» |
| 5xx / sin respuesta | ERP caído | «No se pudo validar con la intranet, intenta más tarde» |

**Efectos que hay que conocer**
- Cada intento fallido desde Frappe **cuenta para el bloqueo del ERP** (son la misma cuenta). Es lo deseado.
- El ERP registra IP y user-agent del intento; los logins hechos desde Frappe se verán con la IP del
  servidor A. Si se quiere la IP real, Frappe puede reenviar `X-Forwarded-For` (el ERP lo lee).
- `/api/auth/*` **sigue respondiendo durante un mantenimiento del ERP** (el filtro de mantenimiento lo exceptúa).

## 2. Perfil: `GET {ERP_API_URL}/api/rh/mi-perfil`

Requiere `Authorization: Bearer <token>` (el del login). Solo token, sin permiso especial.
Código: `backend/src/modules/rh/` (controlador de Mi Perfil).

Regresa el registro del empleado (sin contraseña) con, entre otros:
`numero_empleado`, `nombres`, `apellido_paterno`, `apellido_materno`, `correo_corporativo`,
`empresa_nombre`, `area_nombre`, `subarea_nombre`, `oficina_nombre`, `jefe_nombre`.

- **Durante un mantenimiento del ERP este endpoint responde 503** (no está exceptuado). La app de login
  debe tolerarlo: si el usuario ya existe en Frappe, dejarlo entrar con los datos que ya tiene; si es su
  primera vez, pedirle que intente después.
- Si el empleado no tiene `correo_corporativo`, se necesita una regla (pregunta abierta en el plan).
  Frappe exige un correo único por usuario.
- Acoplamiento: depende del módulo RH del ERP. Si algún día molesta, se pide en el ERP un endpoint propio
  de `auth` (anotado como opcional en `docs/pendientes-erp.md`).

## 3. Permisos

- El ERP autoriza **por permisos, nunca por nombre de rol**. Formato `MODULO_ACCION`.
- Permisos propuestos para este proyecto (aún **no existen** en el ERP, ver `docs/pendientes-erp.md`):
  - `CURSOS_VER`: puede entrar a Cursos (rol Frappe: estudiante, LMS Student).
  - `CURSOS_ADMINISTRAR`: crea y administra cursos (roles Frappe: Course Creator y Moderator).
- La app de login sincroniza los roles de Frappe **en cada inicio de sesión** según los permisos que
  regresa el ERP (si se le quitó el permiso en el ERP, lo pierde aquí al siguiente login).

## 4. Servidores

| Servidor | Papel | Qué hay ahí que **no** se toca |
|---|---|---|
| **B** | Producción del ERP | Todo. Este proyecto no corre en B. |
| **A** | Respaldo y failover del ERP. Aquí vive Comunicalo Learning | Compose y `.env` del ERP (`ERP_RESTART_POLICY=no`), respaldos diarios de `erp_db`, Keycloak, cron de respaldo |

- A publica servicios con **nginx-proxy-manager**; el subdominio de Cursos se da de alta ahí.
- **Failover:** si B falla, el ERP completo se levanta en A (`../grupocomunicalo/database/scripts/RUNBOOK_FAILOVER.md`).
  En ese caso A corre ERP + Frappe a la vez: los límites de memoria de Frappe deben dejar espacio al ERP.
- IPs, usuarios SSH y llaves **no** se escriben en este repo. Están en la documentación privada de Desarrollo.

## 5. Módulo E-learning del ERP

- Es un **repositorio de documentos** (manuales y procedimientos con nomenclatura
  `TIPO-AREA-CONSECUTIVO-MES-AÑO-V{n}`, versiones, autorizadores e inactivación con justificación).
  Doc: `../grupocomunicalo/backend/src/modules/elearning/elearning.md`.
- No se reemplaza: solo se le agrega el enlace «Cursos» hacia esta plataforma.
