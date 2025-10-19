SHELL := /bin/bash

OS := $(shell uname -s)

setup:
    @python preflight.py
ifeq ($(OS),Linux)
    @echo "🐧 Ejecutando setup.sh para Linux..."
    chmod +x setup.sh
    ./setup.sh
else ifeq ($(OS),Darwin)
    @echo "🍎 Ejecutando setup.sh para macOS..."
    chmod +x setup.sh
    ./setup.sh
else
    @echo "🪟 Ejecutando setup.bat para Windows..."
    setup.bat
endif

run:
    docker compose up -d --build

stop:
    docker compose down

backup:
    docker exec inventario_iso27001 python auto_backup.py

restore:
    @echo "🔁 Accede a http://localhost:5000/restaurar"

docs:
    @echo "📄 Accede a http://localhost:5000/apidocs"

clean:
    docker compose down -v
    rm -f backups/restaurado_*.xlsx
