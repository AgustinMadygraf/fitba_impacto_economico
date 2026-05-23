"""
Path: run_web.py
"""

import uvicorn

def main():
    print("=" * 60)
    print(" SISTEMA FITBA - SERVIDOR WEB DE IMPACTO ECONÓMICO MADYGRAF ")
    print("=" * 60)
    print("Iniciando servidor Uvicorn...")
    print("Por favor, abre tu navegador web en: http://localhost:8000")
    print("-" * 60)
    
    # Arrancamos Uvicorn programáticamente
    uvicorn.run(
        "src.infrastructure.web.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
