#!/bin/bash
# Despliegue con alta observabilidad y busteo de caché automático
set -euo pipefail

# Logging con timestamps
log() { echo -e "$(date '+%Y-%m-%d %H:%M:%S') [$1] $2"; }
log_info() { log "\e[32mINFO\e[0m" "$1"; }
log_error() { log "\e[31mERROR\e[0m" "$1"; }

# Trampa para errores fatales
trap 'log_error "Fallo en la línea $LINENO. Comando: $BASH_COMMAND"' ERR

# Medición de pasos críticos
measure_step() {
    local step_name="$1"
    shift
    local start=$(date +%s)
    log_info "Iniciando paso: $step_name"
    "$@"
    local end=$(date +%s)
    log_info "Paso '$step_name' completado en $((end - start)) segundos."
}

# 1. Validaciones Locales
measure_step "Tests" pytest

# 2. Configuración
if [ ! -f .env ]; then
    log_error "El archivo .env no existe."
    exit 1
fi
source .env

: "${VPS_USER:?VPS_USER no definido}"
: "${VPS_IP:?VPS_IP no definido}"
: "${VPS_PORT:?VPS_PORT no definido}"
: "${REMOTE_DIR:?REMOTE_DIR no definido}"

SSH_CMD="ssh -p $VPS_PORT $VPS_USER@$VPS_IP"

# 3. Despliegue
measure_step "Git Push" git push origin main

log_info "Ejecutando operaciones remotas..."
# 1. Despliegue y 2. Actualización de timestamp en remoto
TIMESTAMP=$(date +%s)
$SSH_CMD "cd $REMOTE_DIR &&           echo '[REMOTE] Fetching...' && git fetch origin &&           echo '[REMOTE] Resetting...' && git reset --hard origin/main &&           echo '[REMOTE] Actualizando versión JS (Cache Busting)...' &&           sed -i 's/v=__TIMESTAMP__/v=$TIMESTAMP/g' src/infrastructure/web/static/index.html &&           echo '[REMOTE] Instalando dependencias...' && .venv/bin/pip install -r requirements.txt &&           echo '[REMOTE] Reiniciando servicio...' && sudo systemctl restart fitba-backend"

log_info "Despliegue finalizado exitosamente. Versión cache-bust: $TIMESTAMP"
