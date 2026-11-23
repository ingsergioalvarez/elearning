# Pendientes del lado del ERP

Cambios que este proyecto necesita **en el ERP**. No se hacen desde aquí: se abre el agente en
`../grupocomunicalo` y se sigue su «Flujo obligatorio de un cambio» (rama, prueba local, commit con
`Usuario:`, `main` y ventana de publicación).

Al terminar uno en el ERP, márcalo aquí con la fecha y el commit del ERP.

| # | Cambio en el ERP | Necesario para | Estado |
|---|---|---|---|
| 1 | Permisos `CURSOS_VER` y `CURSOS_ADMINISTRAR`: migración nueva en `backend/src/database/migrations/` + `config_initdb.sql`. Por ahora asignados solo a Desarrollo (opción B). Learning **no** los lee todavía (decisión 0011, etapa 1) | Fase 2/3 | Prompt entregado 2026-11-23 |
| 2 | Botón o tarjeta «Cursos» en el módulo E-learning (y/o sidebar) que abra `https://elearning.grupocomunicalo.mx/login?redirect-to=/lms` en otra pestaña (con sesión activa entra directo; sin sesión muestra el login con número de empleado), visible con `CURSOS_VER`. URL desde configuración, no hardcodeada. **Opción B (2026-11-23):** se publica ya, pero `CURSOS_VER` solo se asigna a Desarrollo hasta abrir Learning a todos | Fase 3 | Prompt entregado 2026-11-23 |
| 3 | Actualizar `elearning.md` del ERP (secciones Flujo de usuario y Preguntas frecuentes) para que Sofía sepa que los cursos están en Cursos | Fase 3 | Pendiente |
| 4 | Entrada en `/CHANGELOG.md` del ERP | Fase 3 | Pendiente |
| 5 | (Opcional) Endpoint propio de `auth` con correo y empresa del empleado, para no depender de `/api/rh/mi-perfil` | Solo si el acoplamiento con RH causa problemas | Opcional |
| 6 | (Futuro) Que el ERP actúe como proveedor OAuth2/OIDC para entrar a Cursos con un clic | Decisión 0005, mejora futura | Futuro |
| 7 | (Futuro) Mostrar en el expediente o Talento los cursos terminados y certificados, leyendo la API de Frappe | Fase 5 | Futuro |
