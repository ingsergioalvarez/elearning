# 0006 — No usar el Keycloak de A

- **Estado:** Aceptada
- **Fecha:** 2026-11-19

## Contexto
En A corre un Keycloak (`/opt/infra/keycloak`) de una arquitectura anterior. El ERP ya no lo usa para el
login (autentica con su propia tabla de empleados y JWT). Corre en modo `start-dev`, y su entrada en el
proxy (`auth.grupocomunicalo.mx`) está rota.

## Decisión
Learning no se conecta a Keycloak ni lo modifica. La identidad viene del ERP (decisión 0005).

## Consecuencias
Si en el futuro se quiere un proveedor de identidad central de verdad, se decide aparte y se reemplazan
0005 y esta decisión.
