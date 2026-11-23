# Registro de decisiones

Una decisión por archivo, numeradas. Una decisión aceptada no se reescribe: se crea otra que la
reemplaza y la vieja se marca «Reemplazada por NNNN».

| # | Decisión | Estado |
|---|---|---|
| [0001](0001-cursos-en-frappe-documentos-en-erp.md) | Cursos en Frappe Learning; documentos se quedan en E-learning del ERP | Aceptada |
| [0002](0002-proyecto-aparte.md) | Proyecto y repositorio aparte del ERP | Aceptada |
| [0003](0003-servidor-a-contenedor-propio.md) | Servidor A, contenedor propio, no crítico | Aceptada |
| [0004](0004-respaldo.md) | Sin respaldo hacia B; respaldo local diario en A (7 días) | Aceptada |
| [0005](0005-login-contra-erp.md) | Login propio en Frappe validando contra el ERP (misma contraseña) | Aceptada (punto 4 precisado por 0011) |
| [0006](0006-no-usar-keycloak.md) | No usar el Keycloak de A | Aceptada |
| [0007](0007-integracion-con-erp.md) | Integración con el ERP: por ahora solo un enlace | Aceptada |
| [0008](0008-version-frappe-lms.md) | Frappe v16 + Learning version-16, etiquetas fijas | Aceptada |
| [0009](0009-sin-entorno-local.md) | Sin entorno local: la Fase 0 y las pruebas se hacen en A | Aceptada |
| [0010](0010-pruebas-login-contra-produccion.md) | Pruebas del login contra el ERP de producción, con condiciones | Aceptada |
| [0011](0011-identidad-y-roles.md) | Identidad por número de empleado; roles en dos etapas | Aceptada |

Plantilla:

```markdown
# NNNN — Título

- **Estado:** Propuesta | Aceptada | Reemplazada por NNNN
- **Fecha:** AAAA-MM-DD

## Contexto
## Decisión
## Consecuencias
```
