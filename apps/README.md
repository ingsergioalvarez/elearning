# apps/

Apps propias de Frappe. **Toda personalización vive aquí**; el código de Frappe y de `lms` no se modifica.

## comunicalo_auth (Fase 2)

Login con número de empleado y contraseña del ERP. Diseño en `docs/decisiones/0005-login-contra-erp.md`,
contrato en `docs/contexto-erp.md`.

Por decidir en la Fase 2, verificando contra la documentación de la versión de Frappe que se fije:
- Cómo reemplazar el login sin tocar el core: sobrescribir el método de login por hooks
  (`override_whitelisted_methods`), o una página de login propia que llame a un método whitelisted
  propio y abra la sesión con el `LoginManager` de Frappe. Elegir la opción soportada oficialmente que
  sobreviva actualizaciones.
- Dónde se configura `ERP_API_URL` (variable de entorno o `site_config.json`).

Requisitos:
- Nunca registrar la contraseña ni el token del ERP.
- Timeout corto hacia el ERP (unos 10 s) y mensajes claros para ERP caído o en mantenimiento.
- Pruebas: primero unitarias con respuestas simuladas del ERP; después contra producción solo con las
  condiciones de la decisión 0010. Identidad y roles: decisión 0011.
