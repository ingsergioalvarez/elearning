# 0001 — Cursos en Frappe Learning; documentos se quedan en E-learning del ERP

- **Estado:** Aceptada (confirmada por el usuario el 2026-11-19, pregunta P1 del plan)
- **Fecha:** 2026-11-19

## Contexto
La idea original fue «reemplazar el módulo E-learning por Frappe Learning». Al revisar el ERP, el módulo
E-learning resultó ser un repositorio de **documentos** corporativos: nomenclatura automática
`TIPO-AREA-CONSECUTIVO-MES-AÑO-V{n}`, versiones, autorizadores, inactivación con justificación y documentos
relacionados. Frappe Learning es una plataforma de **cursos**: lecciones, cuestionarios, avance por
persona, grupos y certificados. Frappe no tiene ese control documental.

## Decisión
- Los cursos y capacitaciones van a Frappe Learning.
- Los documentos controlados siguen en E-learning del ERP.
- La intranet muestra «Documentos» (E-learning) y «Cursos» (enlace a Frappe).

## Consecuencias
- No se migra ni se pierde el control documental existente.
- Un curso puede enlazar a un documento del ERP si hace falta (enlace, no copia).
- Si el usuario decide mover también los documentos, esta decisión se reemplaza y hay que diseñar
  cómo conservar nomenclatura y versiones.
