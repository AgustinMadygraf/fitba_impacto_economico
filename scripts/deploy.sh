#!/bin/bash
# Despliegue con alta observabilidad
set -euo pipefail # Estricto manejo de errores

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
    log_error "El archivo .env no existe. Por favor créalo con las variables necesarias."
    exit 1
fi
source .env

# Validación estricta de variables necesarias
: "${VPS_USER:?VPS_USER no definido en .env}"
: "${VPS_IP:?VPS_IP no definido en .env}"
: "${VPS_PORT:?VPS_PORT no definido en .env}"
: "${REMOTE_DIR:?REMOTE_DIR no definido en .env}"

SSH_CMD="ssh -p $VPS_PORT $VPS_USER@$VPS_IP"

# 3. Despliegue
measure_step "Git Push" git push origin main

log_info "Ejecutando operaciones remotas..."
# Ejecución directa de comandos en remoto
$SSH_CMD "cd $REMOTE_DIR &&           echo '[REMOTE] Fetching...' && git fetch origin &&           echo '[REMOTE] Resetting to origin/main...' && git reset --hard origin/main &&           echo '[REMOTE] Instalando dependencias...' && .venv/bin/pip install -r requirements.txt &&           echo '[REMOTE] Reiniciando servicio...' && sudo systemctl restart fitba-backend"

log_info "Despliegue finalizado exitosamente."
