#!/usr/bin/env bash
# Construye la imagen de Comunicalo Learning con versiones fijas (decisión 0008).
# Uso (en la carpeta de Learning):  bash scripts/construir_imagen.sh
# Lee infra/.env. Usa images/custom/Containerfile de frappe_docker (no "layered": la imagen
# frappe/build no publica etiquetas exactas de Frappe, así que no se podría fijar la versión).
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$RAIZ/infra/.env"
[ -f "$ENV_FILE" ] || { echo "No existe $ENV_FILE"; exit 1; }
set -a; . "$ENV_FILE"; set +a

for v in FRAPPE_VERSION LMS_VERSION PAYMENTS_VERSION FRAPPE_DOCKER_VERSION PYTHON_VERSION IMAGEN_LEARNING; do
  [ -n "${!v:-}" ] || { echo "Falta $v en $ENV_FILE"; exit 1; }
done

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

echo "Construyendo $IMAGEN_LEARNING (Frappe $FRAPPE_VERSION, lms $LMS_VERSION, payments $PAYMENTS_VERSION)"
cd "$FD_DIR"
docker build \
  --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
  --build-arg=FRAPPE_BRANCH="$FRAPPE_VERSION" \
  --build-arg=PYTHON_VERSION="$PYTHON_VERSION" \
  --secret=id=apps_json,src="$APPS_JSON" \
  --tag="$IMAGEN_LEARNING" \
  --file=images/custom/Containerfile .

echo "Listo: $IMAGEN_LEARNING"
