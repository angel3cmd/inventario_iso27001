# 📦 CHANGELOG — Inventario ISO 27001

## [v1.0.0] — 2025-10-19

### 🚀 Primera versión estable

- Docker Compose con volúmenes persistentes (`inventario.db`, `backups/`, `secret.key`)
- Automatización de backups con `auto_backup.py`
- Cifrado Fernet y envío por correo
- Restauración web de archivos `.xlsx.enc`
- Auditoría completa con exportación CSV (firma SHA256) y PDF
- Autenticación por roles (`admin`, `auditor`, `operador`)
- Makefile multiplataforma para despliegue rápido
- `.env.template` para configuración reproducible
- Documentación técnica (`README.md`, `README.dev.md`)
- Scripts de instalación (`setup.sh`, `setup.bat`)
