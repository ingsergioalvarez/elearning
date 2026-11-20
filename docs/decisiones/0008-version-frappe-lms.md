# 0008 — Versión: Frappe v16 + Learning línea version-16, con etiquetas fijas

- **Estado:** Aceptada (el usuario delegó la elección el 2026-11-19)
- **Fecha:** 2026-11-19

## Contexto
Revisado en GitHub el 2026-11-19:
- **Frappe framework:** líneas `version-15` (v15.127.x) y `version-16` (v16.60.x), ambas con soporte.
  v16 lleva más de 60 versiones menores: está madura.
- **Learning (`frappe/lms`)** cambió su numeración el 2026-11-04. Antes era v2.x en `main`
  (última: v2.69.0); ahora sigue la versión del framework:
  - `version-16`: activa (v16.0.0 el 2026-11-04 … v16.3.0 el 2026-11-19).
  - `version-15`: quedó en v15.0.0 el 2026-11-04 sin cambios desde entonces.
  - `main` (v2.x): ya no recibe versiones.
- Learning requiere la app `frappe/payments` (`required_apps`), que también tiene `version-16`.
- Herramienta de despliegue: `frappe_docker` v4.2.0 (2026-10-30).

## Decisión
- Frappe **v16**, Learning línea **version-16** y payments **version-16**. Para construir la imagen, `frappe_docker`.
- Se instala con **etiquetas exactas** (por ejemplo `v16.60.2` / `v16.3.0`), nunca con ramas móviles.
  El día de la instalación se toma el último parche publicado de cada uno y se anota en el CHANGELOG.
- Para payments, que casi no publica etiquetas, se fija el **commit** exacto de `version-16`.
- No se usa `version-15`: es la línea que va de salida y su Learning ya quedó congelado.
- No se usa `develop`: es inestable.
- Las actualizaciones posteriores son a propósito, con respaldo previo y probadas antes en local.

## Consecuencias
- Es la línea con soporte más largo por delante.
- La línea v16 de Learning tiene solo dos semanas y saca versiones seguido. Por eso la Fase 0 debe probar
  a fondo lo que se va a usar: lecciones, cuestionarios, SCORM, certificados y celular.
- Si en la Fase 0 aparece un fallo grave de la v16 de Learning, se reevalúa con una decisión nueva.
