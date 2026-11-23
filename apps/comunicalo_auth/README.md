# comunicalo_auth

Login de Comunicalo Learning con **número de empleado y contraseña del ERP** (decisiones 0005, 0010, 0011).
No modifica Frappe ni lms: reemplaza la página `/login` porque las apps instaladas después tienen prioridad.

## Qué hace
1. `/login` pide «Número de empleado» y «Contraseña» y llama a `comunicalo_auth.login.entrar`
   (máximo 10 intentos por minuto por IP).
2. Valida con `POST {erp_api_url}/api/auth/login` y trae el perfil con `GET {erp_api_url}/api/rh/mi-perfil`.
3. Crea o actualiza el usuario de Frappe: identidad por el campo `numero_empleado`; correo corporativo o
   técnico `<numero>@empleados.grupocomunicalo.local`; si cambia el correo, renombra el usuario sin perder avance.
4. Roles etapa 1: asegura `LMS Student`; nunca quita roles de administrador asignados a mano.
5. Abre la sesión con `LoginManager.login_as`. La contraseña y el token del ERP no se guardan ni se registran.
- `Administrator` entra en la misma pantalla con su contraseña local (emergencias); no pasa por el ERP.
- Quita destinatarios `.local` de la cola de correos (`Email Queue`, before_insert).
- Al instalar/migrar: campos `numero_empleado`, `empresa_erp`, `area_erp` en User y desactiva el registro libre.

## Configuración (site_config, nunca en código)
```bash
bench --site <sitio> set-config erp_api_url https://grupocomunicalo.mx      # sin /api
bench --site <sitio> set-config -p erp_timeout_segundos 10
```

## Pruebas (respuestas simuladas del ERP, sin red ni Frappe)
```bash
python -m unittest discover -s comunicalo_auth/tests -t .
```
`scripts/construir_imagen.sh` las corre también dentro de la imagen.

**Nunca activar `developer_mode` en A:** con él, las trazas de error incluyen variables locales.
