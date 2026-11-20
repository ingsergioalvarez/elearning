# Comunicalo Learning

Plataforma de cursos y capacitación del Grupo Comunicalo, basada en
[Frappe Learning](https://github.com/frappe/lms).

- **Dónde corre:** servidor A, en su propio contenedor. No es crítico: si se cae, la intranet sigue funcionando.
- **Cómo se entra:** con el mismo número de empleado y contraseña del ERP (Frappe valida contra el ERP).
- **Desde la intranet:** el módulo E-learning tiene un enlace «Cursos» que abre esta plataforma.
- **Qué NO es:** el repositorio de documentos (manuales, procedimientos con nomenclatura y versiones).
  Eso sigue en el módulo E-learning del ERP.

## Para empezar a trabajar

1. Lee [`CLAUDE.md`](CLAUDE.md) (reglas) y [`docs/plan-de-trabajo.md`](docs/plan-de-trabajo.md) (en qué vamos).
2. Si trabajas con un agente de IA por primera vez, usa [`PROMPT_INICIAL.md`](PROMPT_INICIAL.md).

## Documentación

- [Decisiones](docs/decisiones/)
- [Contexto del ERP](docs/contexto-erp.md)
- [Pendientes del lado del ERP](docs/pendientes-erp.md)
- [Runbook del servidor A](docs/runbook-servidor-a.md)
- [Historial de cambios](CHANGELOG.md)
