# Prompt inicial para el agente

Copia el bloque de abajo en la primera sesión del agente, abierto **en esta carpeta**
(`comunicalo-learning`). En las sesiones siguientes basta con: «Lee CLAUDE.md y el plan, y dime en qué
vamos y qué sigue».

---

```
Vamos a trabajar en Comunicalo Learning: la plataforma de cursos y capacitación del Grupo Comunicalo,
basada en Frappe Learning (app lms de Frappe), en su propio contenedor en el servidor A, separada del ERP.

Antes de proponer nada, lee completos y en este orden:
1. CLAUDE.md (reglas obligatorias de este repo)
2. CHANGELOG.md
3. docs/plan-de-trabajo.md (fases y preguntas abiertas)
4. docs/decisiones/ (todas; no contradigas una decisión sin proponer otra que la reemplace)
5. docs/contexto-erp.md (contrato de login y perfil con el ERP, servidores)
6. docs/pendientes-erp.md

Contexto clave (ya decidido, está en docs/decisiones):
- Proyecto aparte del ERP. El ERP está en ../grupocomunicalo: puedes LEERLO para confirmar contratos,
  pero NO lo editas desde aquí. Lo que toque al ERP se anota en docs/pendientes-erp.md.
- Corre en el servidor A, contenedor propio, no crítico, sin respaldo hacia B (respaldo local propuesto).
- Login propio en Frappe con número de empleado y la misma contraseña del ERP: Frappe valida contra
  POST /api/auth/login del ERP y trae correo y empresa de GET /api/rh/mi-perfil. Nunca se guarda la contraseña.
- Frappe no se conecta a la base del ERP. No se usa el Keycloak de A. No se modifica el core de Frappe:
  todo va en apps propias (apps/comunicalo_auth).
- En el ERP solo habrá un enlace "Cursos" en E-learning (se hace desde el repo del ERP).

Trabajo de hoy: empezar la Fase 0 (prueba en local).
1. P1, P2 y P3 ya están resueltas (ver plan y decisión 0008: Frappe v16 + lms/payments version-16).
   No hay cursos previos: la prueba se hace con un curso de muestra y un paquete SCORM de muestra.
2. Propón el docker-compose local basado en frappe_docker con la app lms y etiquetas exactas
   (verifica en GitHub cuáles son los últimos parches de la línea v16 ese día y en la documentación
   oficial la forma recomendada de construir la imagen con apps extra).
3. No edites ni ejecutes nada hasta que yo diga "procede". Nada contra servidores de producción.

Reglas de trabajo: respóndeme en español; al terminar cada cambio pregunta "¿Hago el commit? ¿A qué
rama?"; al cerrar la sesión actualiza docs/plan-de-trabajo.md y CHANGELOG.md, y avísame qué quedó
levantado o pendiente.
```
