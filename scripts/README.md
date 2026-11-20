# scripts/

Scripts operativos para el servidor A (se crean en la Fase 1).

- `respaldo_local.sh`: `bench backup --with-files`, retención de 7 días y aviso si falla.
- `verificar.sh` (opcional): estado de contenedores, último respaldo y espacio en disco.

Reglas:
- Los cron llaman `bash <script>`, nunca el `.sh` directo. En el ERP, un `.sh` sin `+x` hizo que los
  respaldos fallaran en silencio durante meses.
- Ningún script borra volúmenes ni toca nada del ERP.
