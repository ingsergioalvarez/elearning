# Changelog — Comunicalo Learning

Historial de cambios significativos. Entrada nueva arriba de todo, con fecha real.

---

## 2026-11-19 — Conexión a A, plantilla .env y skill de despliegue

- `CLAUDE.local.md` (fuera de git): comando SSH a A y carpetas del ERP que no se tocan.
- `infra/.env.example`: variables de Learning (versiones fijas, sitio, MariaDB propia, `ERP_API_URL`,
  límites de memoria). El `.env` del ERP no se copia: Frappe no usa sus secretos.
- Skill `desplegar-learning`: respaldo verificado, actualización y reinicio solo de `-p learning`,
  verificación y registro.
- Riesgo detectado: en A, el ERP está detenido como failover. `docker container prune` o
  `docker system prune` borrarían sus contenedores. Quedó prohibido en `CLAUDE.md` y en la skill.
- Nueva pregunta P12: repositorio remoto y cómo llega el código a A.

## 2026-11-19 — Resueltas P2 y P3: no hay cursos previos; Frappe v16

- **P2:** no existen cursos; se diseñarán desde cero. La Fase 0 se prueba con un curso de muestra y un
  paquete SCORM de muestra.
- **P3 / decisión 0008:** Frappe v16 + Learning y payments en `version-16`, con etiquetas fijas.
  El 2026-11-04 Learning dejó la numeración v2.x (`main`) y ahora sigue la versión del framework;
  `version-15` quedó congelada.
- Nueva pregunta P11: con qué se hará el contenido interactivo. Se decide después de probar SCORM.

## 2026-11-19 — Confirmadas P1 y P8

- **P1 / decisión 0001 aceptada:** el módulo E-learning del ERP se queda como repositorio de documentos;
  Frappe Learning es solo para cursos y capacitaciones.
- **P8 / decisión 0004 aceptada completa:** respaldo local diario en A con 7 días de retención, sin copia a B.
- Siguen abiertas para la Fase 0: P2 (formato de los cursos) y P3 (versión de Frappe/lms a fijar).

## 2026-11-19 — Creación del proyecto y decisiones iniciales

- Se crea el repositorio aparte del ERP para montar Frappe Learning como plataforma de cursos.
- Decisiones registradas en `docs/decisiones/` (0001 a 0007):
  - Frappe Learning para **cursos**; el módulo E-learning del ERP se queda como repositorio de
    **documentos** (propuesta, por confirmar con el usuario).
  - Proyecto y repositorio aparte; en el ERP solo un enlace «Cursos».
  - Servidor A, contenedor propio, no crítico.
  - Sin respaldo hacia B; se propone respaldo local diario en A.
  - Login propio en Frappe que valida número de empleado y contraseña contra `POST /api/auth/login`
    del ERP (misma contraseña). SSO de un clic queda como opción futura.
  - No se usa el Keycloak que corre en A.
- Contrato con el ERP documentado en `docs/contexto-erp.md` (revisado contra el código del ERP ese día).
- Estado: Fase 0 sin iniciar. Aún no hay nada instalado ni en local ni en A.
