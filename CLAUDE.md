# Reglas del proyecto — Comunicalo Learning (cursos y capacitación)

Plataforma de cursos y capacitación del Grupo Comunicalo, basada en **Frappe Learning** (app `lms`
del framework Frappe). Vive en su **propio contenedor en el servidor A**, separada del ERP a propósito:
su mantenimiento no reinicia ni toca la intranet.

> Cualquier persona o asistente de IA (Claude, Copilot, Cursor, Codex u otro) que trabaje aquí sigue
> estas reglas al pie de la letra. Si una regla no se puede cumplir, se detiene y pregunta.

---

## Antes de hacer cualquier cosa (cada sesión)

Leer, en este orden:

1. `CHANGELOG.md`: qué ya se hizo.
2. `docs/plan-de-trabajo.md`: en qué fase vamos y qué sigue.
3. `docs/decisiones/`: decisiones ya tomadas. **No se contradicen en silencio**: si algo debe cambiar,
   se propone y, si la persona acepta, se registra una decisión nueva que reemplaza a la anterior.
4. `docs/contexto-erp.md`: todo lo que este proyecto necesita saber del ERP (login, permisos, servidores).
5. `docs/pendientes-erp.md`: cambios que tocan al ERP y que se hacen **desde el repo del ERP**, no desde aquí.

---

## Flujo obligatorio de un cambio

Cada paso es obligatorio y en este orden. «Procede» autoriza el paso que se está discutiendo, no los siguientes.

0. **Actualizar:** `git pull` antes de tocar nada (si hay remoto).
1. **Revisar** CHANGELOG, plan y decisiones para no duplicar ni contradecir.
2. **Analizar en solo lectura y proponer.** No editar nada hasta que la persona diga «procede».
3. **Hacer el cambio** respetando este documento.
4. **Probar en A** (no hay Docker local, decisión 0009): en el sitio de Learning, antes de abrirlo a usuarios
   y con respaldo previo verificado. El login nunca toca la base del ERP. Si por urgencia no se prueba, el
   commit lo dice: `Sin prueba: <motivo>`.
5. **Commit** en español, chico y enfocado. En el cuerpo, opcional, `Usuario: ...` (qué cambia para quien toma cursos).
6. **Preguntar:** «¿Hago el commit? ¿A qué rama lo subo?». Sin respuesta no se sube nada.
7. **Publicar en el servidor A solo con autorización explícita de la persona en ese momento.** No hay
   ventana de mantenimiento obligatoria (no afecta al ERP), pero sí se avisa si hay gente tomando cursos.
8. **Al cerrar la sesión:** marcar casillas en `docs/plan-de-trabajo.md`, agregar entrada en `CHANGELOG.md`
   si el cambio es significativo y avisar commits sin subir, contenedores locales levantados o pendientes.

---

## Límites con el ERP — Regla crítica

- **Este repositorio no modifica el ERP.** El ERP vive en `../grupocomunicalo` y tiene sus propias reglas
  (`../grupocomunicalo/CLAUDE.md`). Todo lo que requiera tocar el ERP (botón «Cursos», permisos nuevos, etc.)
  se anota en `docs/pendientes-erp.md` y se hace abriendo el agente **en ese repo**, con su flujo.
  Leer el código del ERP para entender un contrato está bien; editarlo desde aquí, no.
- **Frappe nunca se conecta a la base del ERP** (`erp_db` ni su MySQL). Solo habla con el ERP por su API HTTP.
- **En el servidor A no se toca nada del ERP:** ni su `docker-compose`, ni su `.env`
  (ahí `ERP_RESTART_POLICY=no` es intencional: A es respaldo y failover), ni sus respaldos de `erp_db`.
- **No se usa ni se toca el Keycloak que corre en A** (ver `docs/decisiones/0006-no-usar-keycloak.md`).

---

## Producción (servidor A)

- Acceso SSH solo lo tiene Desarrollo (Alexis y Sergio Alberto). El comando de conexión está en
  **`CLAUDE.local.md`** (privado, fuera de git, solo en la máquina de Desarrollo): léelo si existe. Si no
  existe, el agente no intenta conectarse ni adivina datos: pregunta.
- **Para desplegar o actualizar en A se usa la skill `desplegar-learning`** (`.claude/skills/`). Invocarla
  es la autorización para ese despliegue. Fuera de la skill, cada comando que cambie A se pregunta.
- **En A el ERP está detenido a propósito (failover).** Prohibido `docker container prune` y
  `docker system prune`: borrarían sus contenedores. Todo `docker compose` de este proyecto lleva
  `-p learning` y corre en la carpeta de Learning.
- El agente **no ejecuta comandos que cambien el estado de A** (instalar, `docker compose up/down`, editar
  archivos, `bench migrate`, etc.) sin que la persona lo autorice en ese momento. Comandos de solo lectura
  (`df -h`, `free -h`, `docker ps`, logs) solo cuando la persona lo pida.
- **Prohibido:** `docker compose down -v`, `docker volume rm`, `bench drop-site`, `bench --force reinstall`,
  borrar carpetas de `sites/` o de respaldos. Equivale a perder todos los cursos y avances.
- **Antes de actualizar** Frappe o la app `lms`: `bench backup --with-files` y verificar que el archivo existe.
- Versiones **fijas** de imágenes y apps (nunca `latest` ni ramas móviles). Se suben a propósito, una a la vez.
- Todo procedimiento operativo vive en `docs/runbook-servidor-a.md`; si se hace algo nuevo en A, se documenta ahí.

---

## Seguridad y datos

- **La contraseña del ERP nunca se guarda en Frappe**, ni en logs, ni en errores. La app de login solo la
  reenvía al ERP y descarta la respuesta (incluido el JWT) después de usarla.
- Secretos solo en `.env` (fuera de git). `infra/.env.example` lleva los nombres de las variables sin valores.
- El material original de los cursos (videos, paquetes SCORM, PDF fuente) **no va a git**: carpeta
  `contenido/` (ignorada). En git solo va código, configuración y documentación.
- No exponer puertos de MariaDB ni Redis fuera del contenedor.

---

## Personalización de Frappe — Regla obligatoria

- **No se modifica el código de Frappe ni de `lms`.** Toda personalización va en apps propias dentro de
  `apps/` (la primera: `comunicalo_auth`). Así una actualización de Frappe no borra ni rompe lo nuestro.
- Marca (logo, colores azul/gris, nombre) se configura desde la propia administración de Frappe, no con
  cambios de código.
- Idioma `es-MX` y zona horaria `America/Mexico_City` en la configuración del sistema de Frappe.

---

## Estructura de carpetas

| Carpeta / archivo | Para qué es |
|---|---|
| `CLAUDE.md` | Estas reglas. |
| `AGENTS.md` | Remite a `CLAUDE.md` para asistentes que no lo leen solos. |
| `README.md` | Qué es el proyecto, para personas. |
| `CHANGELOG.md` | Historial de cambios significativos (memoria de largo plazo). |
| `PROMPT_INICIAL.md` | Prompt para arrancar la primera sesión del agente. |
| `docs/plan-de-trabajo.md` | Fases con casillas y preguntas abiertas. Se actualiza al cerrar cada sesión. |
| `docs/decisiones/` | Registro de decisiones (una por archivo, numeradas). |
| `docs/contexto-erp.md` | Contrato con el ERP: login, perfil, permisos, servidores. |
| `docs/pendientes-erp.md` | Cambios que se hacen en el repo del ERP, no aquí. |
| `docs/runbook-servidor-a.md` | Cómo se instala, actualiza, respalda y restaura en A. |
| `CLAUDE.local.md` | Conexión al servidor A. **Privado, fuera de git.** |
| `.claude/skills/desplegar-learning/` | Procedimiento de despliegue en A (skill). |
| `infra/` | `docker-compose.yml`, `.env.example`, configuración del proxy. |
| `apps/` | Apps propias de Frappe (`comunicalo_auth`, login contra el ERP). |
| `scripts/` | Scripts operativos (respaldo local, verificación). Los cron llaman `bash <script>`. |
| `contenido/` | Material fuente de cursos. **Ignorado por git.** |

---

## Registro de decisiones

- Una decisión por archivo: `docs/decisiones/NNNN-titulo-corto.md`, con el siguiente número libre.
- Formato: **Estado** (Propuesta / Aceptada / Reemplazada por NNNN), **Fecha** real, **Contexto**,
  **Decisión**, **Consecuencias**.
- Una decisión aceptada no se edita para cambiarla: se crea otra que la reemplaza y se marca la vieja.

## Changelog

Entrada nueva arriba de todo en `CHANGELOG.md`, con fecha real (no relativa), cuando hay: instalación
o actualización en A, cambio en la app de login, decisión de arquitectura, o algo no obvio que se aprendió
a la mala. No copiar el `git log`.

---

## Convenciones

- Todo en español: código propio, documentación, commits y respuestas a la persona.
- Fechas reales (`2026-11-19`), nunca «ayer» o «la semana pasada».
- Nada hardcodeado: URLs del ERP, dominios y secretos van en `.env` o en la configuración de Frappe.

## Filosofía

El objetivo es que la gente tome sus cursos con la misma contraseña del ERP y sin fricción, y que RH
suba cursos sin depender de Desarrollo. Antes de agregar algo: **¿esto simplifica el trabajo del usuario?**
Si no, no se hace.
