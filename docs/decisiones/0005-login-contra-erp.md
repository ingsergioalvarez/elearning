# 0005 — Login propio en Frappe validando contra el ERP (misma contraseña)

- **Estado:** Aceptada (el usuario pidió login propio con la misma contraseña; el mecanismo es la propuesta aceptada).
  El punto 4 (identidad del usuario y roles) lo precisa la decisión 0011 (2026-11-23).
- **Fecha:** 2026-11-19

## Contexto
El usuario quiere que Learning tenga su propia pantalla de login, con la misma contraseña del ERP. El ERP
no es un proveedor OAuth2/OIDC completo: emite un JWT HS256 propio con `JWT_SECRET` y autentica por
número de empleado (`POST /api/auth/login`).

Opciones evaluadas:
1. **Frappe valida contra el ERP** (elegida): no cambia el ERP.
2. ERP como proveedor OIDC para entrar con un clic: más cómodo, pero requiere cambiar el módulo `auth`
   del ERP. Queda como mejora futura.
3. Copiar las contraseñas cifradas del ERP a Frappe: descartada. Se desincronizan al cambiar la contraseña
   y los formatos de cifrado no son los mismos.

## Decisión
App propia `apps/comunicalo_auth`:
1. Pantalla de login de Frappe con «Número de empleado» y «Contraseña».
2. Se reenvía a `POST {ERP_API_URL}/api/auth/login` de servidor a servidor.
3. Si es válida: `GET /api/rh/mi-perfil` con el token para traer nombre, correo, empresa y área.
4. Se crea o actualiza el usuario de Frappe (con una contraseña aleatoria interna que nadie conoce), se
   sincronizan los roles según `CURSOS_VER` / `CURSOS_ADMINISTRAR`, y se abre la sesión de Frappe.
5. El token del ERP y la contraseña se descartan; nunca se guardan ni se registran en logs.

## Consecuencias
- Una sola contraseña: cambios, recuperación, bloqueo (3 intentos) y bajas se manejan en el ERP.
- Si el ERP (B) está caído, nadie entra a Cursos (aceptable: no es crítico).
- Durante un mantenimiento del ERP, el login responde pero el perfil da 503: los usuarios existentes
  entran con sus datos guardados; los nuevos deben esperar.
- Se conserva la cuenta `Administrator` local de Frappe para emergencias.
- Detalle del contrato: `docs/contexto-erp.md`.
