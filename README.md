# 🛡️ Inventario ISO 27001 - Sistema de Auditoría y Restauración

Este proyecto es una aplicación Flask diseñada para gestionar activos, realizar backups cifrados, enviarlos por correo, restaurarlos desde la web y mantener trazabilidad completa conforme a ISO 27001.

---

## 🚀 Funcionalidades principales

- Gestión de activos con autenticación
- Backup cifrado con clave segura (`Fernet`)
- Envío automático por correo
- Restauración web de archivos `.xlsx.enc`
- Registro de auditoría en SQLite
- Exportación de auditoría como CSV y PDF
- Firma digital SHA256 para integridad
- Filtros por fecha y destino en la vista web
- Protección por rol (solo admins pueden exportar)

---

## 🧱 Estructura del proyecto

inventario_iso27001/ 
├── app.py 
├── models.py 
├── auth.py 
├── dashboard.py 
├── export.py 
├── decrypt_file.py 
├── generar_pdf_auditoria.py 
├── templates/ 
│ ├── index.html 
│ ├── login.html 
│ ├── dashboard.html 
│ ├── restaurar.html 
│ └── auditoria.html 
├── backups/ 
├── secret.key 
├── inventario.db 
├── requirements.txt


---

## 🔐 Seguridad

- Clave `secret.key` montada como volumen externo
- Auditoría de cada restauración y envío
- Exportaciones protegidas por rol
- Firma digital SHA256 incluida en CSV

---

## 📦 Exportaciones

- `/auditoria/exportar` → CSV con firma
- `/auditoria/pdf` → PDF profesional
- Filtros disponibles en `/auditoria` por fecha y destino

---

## 🧪 Requisitos

- Python 3.10+
- Docker + Docker Compose
- Paquetes: Flask, cryptography, reportlab, python-dotenv

---

## 🧠 Autor

Miguel — Administrador de sistemas e ingeniero de automatización con enfoque en seguridad, trazabilidad y cumplimiento ISO.

---

#########################################

## 🚀 Instalación automática

Después de clonar el repositorio:

### En Linux/macOS:

```bash
bash setup.sh

## O con Makefile:

Bash

make init
make run

### En Windows:

setup.bat

Esto instalará dependencias, generará la clave secret.key, inicializará la base de datos y levantará el sistema en Docker.

#############################################################

V2

Sistema web desarrollado en Flask para gestionar activos, realizar respaldos cifrados, restaurarlos desde la web y mantener trazabilidad completa conforme a ISO 27001. Incluye autenticación por roles, exportación segura, filtros de auditoría y panel centralizado.

Funcionalidades principales
🔐 Autenticación con roles (admin, auditor, operador)

🏷️ Gestión de activos con carga y visualización

🔁 Restauración de backups cifrados .xlsx.enc

🧾 Registro de auditoría con fecha, archivo y destino

📊 Dashboard con métricas de inventario

📥 Exportación de auditoría como CSV (con firma SHA256) y PDF profesional

🔍 Filtros por fecha y destino en la vista de auditoría

🔓 Logout y navegación segura

Estructura del proyecto


inventario_iso27001/
├── app.py
├── auth.py
├── models.py
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
├── setup.sh
├── setup.bat
├── requirements.txt


Roles de usuario


Usuario     Contraseña      Rol         Acceso a
admin	    admin123	    Admin	    Todo: inventario, auditoría, restaurar, exportar
auditor	    auditor123	    Auditor	    Solo auditoría
operador	operador123	    Operador	Inventario, restaurar, dashboard

Instalación automática

En Linux/macOS:

Bash

git clone https://github.com/tuusuario/inventario_iso27001.git
cd inventario_iso27001
bash setup.sh


En Windows:

setup.bat

Esto instalará dependencias, generará la clave secret.key, inicializará la base de datos y levantará el sistema en Docker.




Ruta	    Descripción	            Protegida por rol
/login	    Inicio de sesión	    No
/home	    Panel principal con navegación	Sí
/	        Inventario de activos	operador, admin
/agregar	Agregar activo	        operador, admin
/dashboard	Métricas del inventario	operador, admin
/restaurar	Listar backups cifrados	operador, admin
/restaurar/<file>	Restaurar archivo y registrar auditoría	operador, admin
/auditoria	Ver historial con filtros	auditor, admin
/auditoria/exportar	Exportar CSV con firma digital	admin
/auditoria/pdf	Exportar PDF profesional	admin
/logout	    Cerrar sesión	           Sí


Exportaciones
CSV con firma SHA256: /auditoria/exportar

PDF profesional: /auditoria/pdf

Excel de inventario: /exportar

🧪 Requisitos
Python 3.10+

Docker + Docker Compose

Paquetes: Flask, cryptography, reportlab, python-dotenv

Instalación automática con setup.sh o setup.bat.

🧠 Autor
Miguel — Administrador de sistemas e ingeniero de automatización con enfoque en seguridad, trazabilidad y cumplimiento ISO 27001. Especializado en automatización de backups, despliegue CI/CD y gestión de activos.

###################################################

v3

plaintext

inventario_iso27001/
├── app.py
├── models.py
├── backup.py
├── auto_backup.py
├── config.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.template
├── Makefile
├── inventario.db         ← generado por `make setup`
├── backups/              ← carpeta persistente
└── secret.key            ← clave montada o generada


Guía de despliegue para nuevos equipos

markdown

## 🚀 Despliegue rápido

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/inventario_iso27001.git
cd inventario_iso27001


Crea tu archivo .env:

bash 

cp .env.template .env


Prepara el entorno:

bash 

make setup

Levanta los contenedores:

bash 

make build
make up


Accede a la app:

http://localhost:5000


##############################################################
v4

Documentación del proyecto

# Inventario ISO 27001

Sistema web para gestionar activos de TI conforme a estándares de seguridad y auditoría. Incluye autenticación, cifrado de backups, exportación de auditoría y documentación Swagger protegida.

## 🚀 Requisitos

- Python 3.11+
- Docker y Docker Compose
- Make (Linux/macOS) o PowerShell (Windows)
- Navegador web

## ⚙️ Instalación rápida

```bash
make setup
make run

Endpoints principales

Endpoints principales
/login: acceso seguro

/: inventario de activos

/dashboard: métricas

/auditoria: historial de envíos

/restaurar: restaurar backups cifrados

/exportar: exportar inventario

/auditoria/exportar: exportar CSV con firma

/auditoria/pdf: exportar PDF

/apidocs: documentación Swagger (requiere login)

Seguridad
Autenticación por sesión

Cifrado AES de backups

Auditoría de restauraciones

Protección de documentación

Estructura

inventario_iso27001/
├── app.py
├── models.py
├── auth.py
├── dashboard.py
├── export.py
├── decrypt_file.py
├── generar_pdf_auditoria.py
├── templates/
├── swagger/
├── backups/
├── .env.template
├── Makefile
├── setup.sh
├── setup.bat


Mantenimiento
make backup: ejecuta backup cifrado

make restore: lista backups disponibles

make docs: abre Swagger UI

make clean: elimina contenedores y volúmenes

🧑‍💻 Autor
Miguel — Arquitecto DevOps, apasionado por la automatización, seguridad y experiencia de desarrollo.


---

## 🛠️ `Makefile` — Automatización multiplataforma

```makefile
SHELL := /bin/bash

setup:
    @echo "🔧 Configurando entorno..."
    cp -n .env.template .env || true
    chmod +x setup.sh
    ./setup.sh

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


#############
## Instalación local del proyecto

Este proyecto requiere Python 3.11 para evitar problemas de compatibilidad con algunas dependencias como pandas y numpy.

### Repositorio y creación de carpeta principal
git clone https://github.com/tu-usuario/inventario_iso27001.git
cd inventario_iso27001


### 🔧 Pasos para instalar y ejecutar localmente:

1. **Instalar Python 3.11**  
   Descárgalo desde [python.org](https://www.python.org/downloads/release/python-3110/) y asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

2. **Crear un entorno virtual**  
   Abre una terminal (CMD o PowerShell) y ejecuta:

   ```bash
   py -3.11 -m venv inventario-env
   inventario-env\Scripts\activate


En Git Bash, usa:

bash
source inventario-env/Scripts/activate
Instalar dependencias Una vez activado el entorno virtual, instala las dependencias con:

bash
pip install -r requirements.txt

Configurar variables de entorno
Crea un archivo .env basado en .env.example:

bash
cp .env.example .env

Ejecutar el proyecto Usa el comando correspondiente para iniciar la aplicación. Por ejemplo:


Inicializar base de datos y claves
bash
python init.py

bash
python app.py
(Ajusta este comando si el archivo principal tiene otro nombre.)

Accede a http://localhost:5000 en tu navegador.