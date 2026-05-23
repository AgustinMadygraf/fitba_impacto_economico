#!/bin/bash
log_info() { echo -e "\e[32m[INFO]\e[0m $1"; }
log_error() { echo -e "\e[31m[ERROR]\e[0m $1"; }
if [ -f .env ]; then source .env; fi
VPS_USER=${VPS_USER:-root}
VPS_IP=${VPS_IP:-168.181.184.103}
VPS_PORT=${VPS_PORT:-5932}
REMOTE_DIR=${REMOTE_DIR:-~/fitba_impacto_economico}
BACKEND_CMD=".venv/bin/python3.11 .venv/bin/uvicorn src.infrastructure.web.app:app --host 127.0.0.1 --port 8011 > server.log 2>&1 &"
SSH_CMD="ssh -p $VPS_PORT $VPS_USER@$VPS_IP"
log_info "Iniciando despliegue..."
git push origin main
if [ -f .env ]; then rsync -avz -e "ssh -p $VPS_PORT" .env $VPS_USER@$VPS_IP:$REMOTE_DIR/; fi
$SSH_CMD "cd $REMOTE_DIR && git pull origin main && ./restart_backend.sh"
