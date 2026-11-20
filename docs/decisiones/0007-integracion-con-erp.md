# 0007 — Integración con el ERP: por ahora solo un enlace

- **Estado:** Aceptada (decisión del usuario)
- **Fecha:** 2026-11-19

## Contexto
El usuario pidió que desde E-learning del ERP solo se cree el enlace hacia Learning.

## Decisión
- En el ERP: botón o tarjeta «Cursos» que abre Learning en otra pestaña, visible con `CURSOS_VER`, con la
  URL en configuración (no hardcodeada).
- Ninguna base compartida. Si después se quieren ver avances o certificados en el ERP, se leen por la API
  REST de Frappe (fase 5 del plan).

## Consecuencias
- El cambio en el ERP es mínimo y se hace desde su repo (`docs/pendientes-erp.md`).
- La persona inicia sesión otra vez al entrar a Cursos (con la misma contraseña), hasta que se haga el
  login de un clic.
