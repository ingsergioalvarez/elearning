#!/usr/bin/env bash
# Construye la imagen de Comunicalo Learning con versiones fijas (decisión 0008), en dos capas:
#   1. IMAGEN_BASE: Frappe + payments + lms con images/custom/Containerfile de frappe_docker
#      (no "layered": frappe/build no publica etiquetas exactas de Frappe). Se omite si ya existe.
#   2. IMAGEN_LEARNING: IMAGEN_BASE + apps propias (apps/comunicalo_auth), con infra/Containerfile.comunicalo.
#      Al final corre las pruebas unitarias de la app dentro de la imagen.
# Uso (en la carpeta de Learning):  bash scripts/construir_imagen.sh
# Lee infra/.env.
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$RAIZ/infra/.env"
[ -f "$ENV_FILE" ] || { echo "No existe $ENV_FILE"; exit 1; }
set -a; . "$ENV_FILE"; set +a

for v in FRAPPE_VERSION LMS_VERSION PAYMENTS_VERSION FRAPPE_DOCKER_VERSION PYTHON_VERSION IMAGEN_BASE IMAGEN_LEARNING; do
  [ -n "${!v:-}" ] || { echo "Falta $v en $ENV_FILE"; exit 1; }
done
[ "$IMAGEN_BASE" != "$IMAGEN_LEARNING" ] || { echo "IMAGEN_BASE e IMAGEN_LEARNING deben ser distintas"; exit 1; }

# --- Capa 1: base ---
if docker image inspect "$IMAGEN_BASE" >/dev/null 2>&1; then
  echo "Ya existe $IMAGEN_BASE; no se reconstruye."
else
  BUILD_DIR="$RAIZ/build"
  FD_DIR="$BUILD_DIR/frappe_docker-$FRAPPE_DOCKER_VERSION"
  mkdir -p "$BUILD_DIR"
  if [ ! -d "$FD_DIR" ]; then
    git clone --depth 1 --branch "$FRAPPE_DOCKER_VERSION" https://github.com/frappe/frappe_docker "$FD_DIR"
  fi
  # apps.json generado desde .env: las versiones viven en un solo lugar.
  APPS_JSON="$BUILD_DIR/apps.json"
  cat > "$APPS_JSON" <<EOF
[
  {"url": "https://github.com/frappe/payments", "branch": "$PAYMENTS_VERSION"},
  {"url": "https://github.com/frappe/lms", "branch": "$LMS_VERSION"}
]
EOF
  echo "Construyendo $IMAGEN_BASE (Frappe $FRAPPE_VERSION, lms $LMS_VERSION, payments $PAYMENTS_VERSION)"
  (cd "$FD_DIR" && docker build \
    --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
    --build-arg=FRAPPE_BRANCH="$FRAPPE_VERSION" \
    --build-arg=PYTHON_VERSION="$PYTHON_VERSION" \
    --secret=id=apps_json,src="$APPS_JSON" \
    --tag="$IMAGEN_BASE" \
    --file=images/custom/Containerfile .)
fi

# --- Capa 2: apps propias ---
echo "Construyendo $IMAGEN_LEARNING sobre $IMAGEN_BASE (apps/comunicalo_auth)"
docker build \
  --build-arg=IMAGEN_BASE="$IMAGEN_BASE" \
  --tag="$IMAGEN_LEARNING" \
  --file="$RAIZ/infra/Containerfile.comunicalo" \
  "$RAIZ/apps/comunicalo_auth"

echo "Pruebas unitarias de comunicalo_auth dentro de la imagen"
docker run --rm --entrypoint "" -w /home/frappe/frappe-bench/apps/comunicalo_auth "$IMAGEN_LEARNING" \
  /home/frappe/frappe-bench/env/bin/python -m unittest discover -s comunicalo_auth/tests -t .

echo "Listo: $IMAGEN_LEARNING"
