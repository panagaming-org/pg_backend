#!/bin/bash

# ============================================
# 🚀 Script de despliegue automatizado para Pana Gaming
# ============================================
# Crea la red Docker si no existe, construye imágenes y levanta contenedores
# Compatible con docker-compose y docker compose (v2)
# ============================================

# === CONFIGURACIÓN ===
NETWORK_NAME="mc-block-net"
SUBNET="172.90.0.0/16"
SERVICE_NAME="png_image_gestor"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# === COLORES PARA LA TERMINAL ===
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # Sin color

# === FUNCIONES AUXILIARES ===
log() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[ADVERTENCIA]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1"
  exit 1
}

ok() {
  echo -e "${GREEN}[OK]${NC} $1"
}

# === VERIFICAR DEPENDENCIAS ===
command -v docker >/dev/null 2>&1 || error "Docker no está instalado o no está en PATH."
command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || error "docker-compose no está disponible."

# === CREAR RED SI NO EXISTE ===
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    log "La red $NETWORK_NAME no existe. Creándola..."
    sudo docker network create --driver bridge --subnet="$SUBNET" "$NETWORK_NAME" && ok "Red $NETWORK_NAME creada correctamente."
else
    ok "La red $NETWORK_NAME ya existe. Continuando..."
fi

# === CONSTRUIR IMÁGENES ===
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
    log "Construyendo imágenes desde $DOCKER_COMPOSE_FILE..."
    sudo docker compose build || sudo docker-compose build || error "Error al construir las imágenes."
else
    warn "No se encontró $DOCKER_COMPOSE_FILE. Construyendo imagen manualmente..."
    sudo docker build -t "$SERVICE_NAME" . || error "Error al construir la imagen manual."
fi

# === LEVANTAR CONTENEDORES ===
log "Levantando contenedores..."
sudo docker compose up -d || sudo docker-compose up -d || error "Error al levantar los contenedores."

# === LIMPIEZA OPCIONAL ===
if [ "$1" == "--clean" ]; then
    warn "Limpiando contenedores e imágenes no usadas..."
    sudo docker system prune -f
    sudo docker volume prune -f
    ok "Sistema Docker limpio."
fi

# === MOSTRAR ESTADO FINAL ===
ok "Todo listo 🚀"
echo ""
log "Contenedores activos:"
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

log "Red Docker:"
sudo docker network inspect "$NETWORK_NAME" --format "{{.Name}} - {{.Id}}"
