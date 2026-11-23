# 0011 — Identidad del usuario y roles en Learning

- **Estado:** Aceptada (decisión del usuario, 2026-11-23). Precisa el punto 4 de la decisión 0005.
- **Fecha:** 2026-11-23

## Contexto
En Frappe el ID del usuario es su correo, y Frappe exige un correo único. En el ERP la identidad estable es
el número de empleado, y no todos tienen `correo_corporativo` (pregunta P7). Además, los permisos
`CURSOS_VER` y `CURSOS_ADMINISTRAR` aún no existen en el ERP (`docs/pendientes-erp.md`, pendiente 1).

## Decisión

### Identidad
- El usuario de Frappe se identifica por **`username = numero_empleado`** (estable), **no por el correo**.
- Correo del usuario: `correo_corporativo` del ERP. Si no tiene, uno técnico:
  `<numero_empleado>@empleados.grupocomunicalo.local`, que nunca recibe correos.
- Si después el empleado recibe correo corporativo o se lo cambian, la app **renombra** el usuario
  (`rename_doc`) en el siguiente login: no se duplica ni pierde su avance, inscripciones ni certificados.
- No se envía correo de bienvenida al crear usuarios, ni ningún correo a direcciones `.local`, para no
  llenar la cola de errores de envío.

### Roles, etapa 1 (mientras el ERP no tenga `CURSOS_VER` / `CURSOS_ADMINISTRAR`)
- Todo empleado **activo** que entre con éxito queda como estudiante (`LMS Student`).
- Los administradores de cursos (RH, Calidad) se asignan **a mano** en Learning (`Course Creator`,
  `Moderator`).
- La sincronización **no toca** los roles de administrador.

### Roles, etapa 2 (cuando el ERP tenga los permisos)
- El ERP pasa a ser la **única fuente** de roles: en cada login se sincronizan según `CURSOS_VER` y
  `CURSOS_ADMINISTRAR`.
- **Antes de activar la sincronización**, se dan en el ERP esos permisos a quienes hoy son administradores
  a mano en Learning. Si no se hace, su siguiente login les quitaría el rol.
- La activación es un ajuste de configuración de la app (no automático por detectar el permiso) y se
  registra en el CHANGELOG con la lista de administradores migrados.

## Consecuencias
- El cambio de correo no rompe la cuenta ni el historial del empleado.
- Mientras se esté en la etapa 1, quitarle el acceso de administrador a alguien se hace a mano en Learning.
- La cuenta `Administrator` local sigue siendo solo para emergencias.
