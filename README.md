# Inventario ISO 27001 — Sistema de Auditoría y Restauración

Aplicación web desarrollada en Flask para gestionar activos de TI conforme a estándares de seguridad y trazabilidad. Incluye autenticación por roles, backups cifrados, restauración web, exportación segura y documentación protegida.

---

## Funcionalidades principales

- Autenticación con roles (admin, auditor, operador)
- Gestión de activos con carga, edición y visualización
- Restauración de backups cifrados `.xlsx.enc`
- Registro de auditoría con fecha, archivo y destino
- Dashboard con métricas de inventario
- Exportación de auditoría como CSV (con firma SHA256) y PDF profesional
- Filtros por fecha y destino en la vista de auditoría
- Logout y navegación segura

---

## Estructura del proyecto

inventario_iso27001/
├── app.py
├── models.py
├── auth.py
├── dashboard.py
├── export.py
├── decrypt_file.py
├── generar_pdf_auditoria.py
├── init_db.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── restaurar.html
│   ├── auditoria.html
│   └── home.html
├── backups/
├── secret.key
├── inventario.db
├── setup.sh / setup.bat
├── requirements.txt
├── Makefile
├── .env.template

---

## Seguridad

- Clave `secret.key` montada como volumen externo
- Cifrado AES con `Fernet` para backups
- Firma digital SHA256 en exportaciones
- Auditoría completa de restauraciones y envíos
- Protección por rol en rutas sensibles
- Documentación Swagger protegida por login

---

## Roles de usuario

| Usuario   | Contraseña   | Rol      | Acceso a                                      |
|-----------|--------------|----------|-----------------------------------------------|
| admin     | admin123     | Admin    | Todo: inventario, auditoría, restaurar, exportar |
| auditor   | auditor123   | Auditor  | Solo auditoría                                |
| operador  | operador123  | Operador | Inventario, restaurar, dashboard              |

---

## Exportaciones

| Ruta                  | Descripción                        | Protegida por rol |
|-----------------------|------------------------------------|-------------------|
| `/auditoria/exportar` | Exportar CSV con firma digital     | admin             |
| `/auditoria/pdf`      | Exportar PDF profesional           | admin             |
| `/exportar`           | Exportar inventario en Excel       | admin             |

---

## Instalación rápida

### Linux/macOS

- git clone https://github.com/tu-usuario/inventario_iso27001.git
- cd inventario_iso27001
- bash setup.sh

### Windows

PowerShell

- setup.bat

### O con Makefile

Bash

- make setup
- make run

## DB

### Inicializar base de datos y claves

Bash

- python init.py

### Docker

Bash

Docker compose build

Docker compose up

### Para Docker con Depuración

Bash

Docker compose up --build

### Finalmente
Accede a http://localhost:5000 en tu navegador.

## Problemas comunes

**Instalar Python 3.11**  
   Descárgalo desde [python.org](https://www.python.org/downloads/release/python-3110/) y asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

---

## Requisitos
- Python 3.11+
- Docker y Docker Compose
- Make (Linux/macOS) o PowerShell (Windows)
- Navegador web moderno

---

## Comandos Makefile


setup:      Inicializa entorno y base de datos
run:        Levanta contenedores
stop:       Detiene contenedores
backup:     Ejecuta backup cifrado
restore:    Accede a restauración web
docs:       Abre Swagger UI
clean:      Elimina contenedores y volúmenes

---

## Restauración y auditoría

- Restaurar backups desde /restaurar/<archivo>
- Registrar automáticamente cada restauración en SQLite
- Visualizar historial en /auditoria
- Filtrar por fecha y destino
- Exportar como CSV o PDF

---

## Documentación Swagger

- Disponible en /apidocs (requiere login)

---

## Autor

Miguel — Arquitecto DevOps y administrador de sistemas, especializado en automatización, trazabilidad y cumplimiento ISO 27001 con enfoque en seguridad.