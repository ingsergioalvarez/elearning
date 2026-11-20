# 0009 — Sin entorno local: la Fase 0 y las pruebas se hacen en A

- **Estado:** Aceptada (decisión del usuario, 2026-11-20)
- **Fecha:** 2026-11-20

## Contexto
`CLAUDE.md` y el plan pedían probar todo primero en Docker en la máquina de desarrollo. El usuario indicó
que no se usará Docker local: Learning solo existirá en el servidor A. A tiene recursos de sobra para
un servicio no crítico (2 núcleos, 7.8 GB de RAM, 77 GB libres el 2026-11-20).

## Decisión
- La Fase 0 (curso de muestra, prueba SCORM, celular) se hace directamente en A.
- La imagen se construye en A (`scripts/construir_imagen.sh`, en `/opt/apps/learning`), con el clon de
  `frappe_docker` en `/opt/apps/learning/build/`.
- Mientras no exista el subdominio (P5), Learning escucha solo en `127.0.0.1:8090` de A y se prueba por
  túnel SSH. Nada se publica hacia internet sin autorización.
- Todo vive en `/opt/apps/learning`, proyecto de compose `learning`, con red y volúmenes propios.
  No se toca ningún otro proyecto, contenedor, volumen ni respaldo de A.

## Consecuencias
- Reemplaza el paso 4 de «Flujo obligatorio de un cambio» de `CLAUDE.md` («Probar en local»): las
  pruebas se hacen en A, en el sitio de Learning, antes de abrirlo a usuarios.
- Como no hay copia local, cada actualización lleva respaldo previo verificado (ya obligatorio).
- La Fase 2 (login contra el ERP) no podrá probarse contra el ERP local desde Docker local; se definirá
  contra qué ERP se prueba (P6) sin usar nunca la base del ERP.
- La compilación de la imagen en A consume CPU y RAM unos 30–45 minutos; se hace fuera de horario si hay
  gente tomando cursos.
