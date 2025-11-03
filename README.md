## ISO 27001 Inventory — Audit and Restoration System

A Flask-based web application designed to manage IT assets in compliance with ISO 27001 security and traceability standards. It includes role-based authentication, encrypted backups, web-based restoration, secure export options, and protected documentation.

---

## Key Features

- Role-based authentication (admin, auditor, operator)
- Asset management with upload, edit, and visualization
- Restoration of encrypted `.xlsx.enc` backups
- Audit logging with date, file, and destination
- Inventory dashboard with metrics
- Audit export as CSV (with SHA256 signature) and professional PDF
- Filters by date and destination in the audit view
- Secure logout and navigation

---

## Project Structure

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

## Security

- `secret.key` mounted as an external volume
- AES encryption with `Fernet` for backups
- SHA256 digital signature on exports
- Full audit trail for restorations and file transfers
- Role-based protection for sensitive routes
- Swagger documentation protected by login

---

## User Roles

| Username  | Password     | Role     | Access Scope                                  |
|-----------|--------------|----------|-----------------------------------------------|
| admin     | admin123     | Admin    | Full access: inventory, audit, restore, export |
| auditor   | auditor123   | Auditor  | Audit view only                               |
| operator  | operador123  | Operator | Inventory, restore, dashboard                 |

---

## Export Options

| Route                 | Description                         | Role Protected |
|----------------------|-------------------------------------|----------------|
| `/auditoria/exportar`| Export audit as signed CSV          | admin          |
| `/auditoria/pdf`     | Export audit as professional PDF    | admin          |
| `/exportar`          | Export inventory as Excel file      | admin          |

---

## Quick Installation

### Linux/macOS

Bash

- git clone https://github.com/your-username/inventario_iso27001.git
- cd inventario_iso27001
- bash setup.sh

### Windows (PowerShell)

PowerShell

- setup.bat

### Or with Makefile

Bash

- make setup
- make run

---

## Database Setup

### Initialize database and keys

Bash

- python init.py

---

## Docker

Bash

Docker compose build

Docker compose up

### Docker with Debug Mode

Bash

Docker compose up --build

---

## Access

Access the App at http://localhost:5000

## Common Issues

**Install Python 3.11**  
   Download from [python.org](https://www.python.org/downloads/release/python-3110/) and make sure to check "Add Python to PATH" during installation

---

## Requirements
- Python 3.11+
- Docker y Docker Compose
- Make (Linux/macOS) or PowerShell (Windows)
- Modern web browser

---

## Makefile Commands


setup:      Initializes environment and database
run:        Start containers
stop:       Stop containers
backup:     Executes encrypted backup
restore:    Opens web restoration interface
docs:       Opens Swagger UI
clean:      Remove containers and volumes

---

## Restoration & Audit

- Restore backups from /restaurar/<file>
- Automatically log each restoration in SQLite
- View audit history at /auditoria
- Filter by date and destination
- Export as CSV or PDF
---

## Swagger Documentation

- Available at /apidocs (login required)

---

## Author

Mikel — DevOps Architect and Systems Administrator, specialized in automation, traceability, and ISO 27001 compliance with a strong focus on security.