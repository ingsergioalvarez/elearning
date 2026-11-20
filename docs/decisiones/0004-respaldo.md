# 0004 — Respaldo: sin copia a B, respaldo local diario en A

- **Estado:** Aceptada completa: sin copia a B y respaldo local diario con 7 días de retención (confirmado por el usuario el 2026-11-19, P8).
- **Fecha:** 2026-11-19

## Contexto
El usuario decidió que Learning vive solo en A, sin respaldo hacia B, por no ser crítico. Aun así, los
cursos, cuestionarios y el avance de las personas son horas de trabajo de RH difíciles de rehacer.

## Decisión
- No se copia nada hacia B.
- `bench backup --with-files` diario en A, con 7 días de retención, en una carpeta propia
  (no la de respaldos de `erp_db`). El cron llama `bash <script>` (lección del ERP: un `.sh` sin `+x` hizo
  que los respaldos fallaran en silencio de agosto a noviembre de 2026).
- Antes de cada actualización, respaldo manual verificado.

## Consecuencias
- Si se pierde el disco de A, se pierde Learning (riesgo aceptado). Los originales de los cursos deben
  conservarse fuera (carpeta `contenido/` local o el lugar que indique RH) para poder recargarlos.
