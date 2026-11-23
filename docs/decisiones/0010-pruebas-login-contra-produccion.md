# 0010 — Pruebas del login contra el ERP de producción, con condiciones

- **Estado:** Aceptada (decisión del usuario, 2026-11-23)
- **Fecha:** 2026-11-23

## Contexto
`CLAUDE.md` pedía probar el login solo contra el ERP local. Con la decisión 0009 no hay entorno local:
Learning vive en A y no puede alcanzar un ERP que corra en la máquina de desarrollo. La única API del ERP
alcanzable desde A es la de producción (`https://grupocomunicalo.mx`).

## Decisión
Las pruebas de `apps/comunicalo_auth` contra el ERP de producción se permiten, solo con estas condiciones:

1. **Primero sin producción.** La app se desarrolla y se prueba lo más posible con pruebas unitarias que
   simulan las respuestas del ERP: login 200, 400, 401, 403; perfil 200 y 503; ERP caído y timeout.
2. **Camino feliz:** lo valida el usuario (Sergio Alberto) con su propia cuenta, escribiendo la contraseña
   en el navegador.
3. **Caminos de error** (contraseña mala, bloqueo por 3 intentos): con un **empleado de prueba** dado de
   alta por RH, que no aparezca en nómina ni en reportes. Al terminar, RH lo inactiva.
4. **Nunca** se pide una contraseña por chat, ni se escribe en comandos, logs, archivos o commits.
5. Las pruebas solo usan la API HTTP del ERP. Nunca su base de datos.

## Consecuencias
- Precisa el paso 4 del flujo de `CLAUDE.md` para el login.
- Cada intento fallido de prueba cuenta para el bloqueo del ERP (es la misma cuenta): por eso los errores
  se prueban con el empleado de prueba y no con cuentas reales.
- Los intentos aparecerán en el registro de accesos del ERP con la IP de A.
- Pendiente con RH: alta del empleado de prueba antes de probar los caminos de error, y su inactivación al terminar.
