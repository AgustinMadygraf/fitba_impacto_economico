#!/bin/bash
# Script centralizado para ejecutar tests o iniciar el servidor
# Uso: ./run.sh [start|test]

CMD=${1:-start}

cd backend
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

if [ "$CMD" == "test" ]; then
    pytest
elif [ "$CMD" == "start" ]; then
    export PYTHONPATH=$PYTHONPATH:$PWD
    echo "============================================================"
    echo " SISTEMA FITBA - SERVIDOR WEB DE IMPACTO ECONÓMICO MADYGRAF "
    echo "============================================================"
    echo "Iniciando servidor Uvicorn..."
    echo "Por favor, abre tu navegador web en: http://localhost:8000"
    echo "------------------------------------------------------------"
    uvicorn src.infrastructure.web.app:app --host 127.0.0.1 --port 8000 --reload --log-level info
fi