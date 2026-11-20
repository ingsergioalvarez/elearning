# infra/

Configuración para levantar Frappe Learning (se crea en la Fase 0).

Contenido previsto:
- `docker-compose.yml`: basado en el repositorio oficial `frappe_docker`, con la app `lms`, MariaDB,
  Redis, workers y scheduler. **Versiones fijas** (nada de `latest`). `restart: unless-stopped`, logging
  `json-file` (20m × 3) y límites de memoria.
- `.env.example`: nombres de variables sin valores (contraseña de MariaDB, `ERP_API_URL`, dominio del sitio…).
  El `.env` real nunca se sube a git.
- `proxy.md`: cómo quedó dada de alta la entrada en nginx-proxy-manager de A (sin secretos).

Si se necesita una imagen propia (para incluir `apps/comunicalo_auth`), su `Containerfile` y el
`apps.json` también van aquí.
