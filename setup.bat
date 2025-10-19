@echo off
echo 🔧 Instalando dependencias...
pip install -r requirements.txt

echo 🔐 Generando clave secreta...
IF NOT EXIST secret.key (
    python -c "from cryptography.fernet import Fernet; open('secret.key', 'wb').write(Fernet.generate_key())"
    echo ✅ Clave generada: secret.key
) ELSE (
    echo 🔑 Clave ya existe: secret.key
)

echo 🧱 Inicializando base de datos...
python init_db.py

echo 🐳 Levantando contenedor Docker...
docker compose up -d

echo ✅ Sistema listo en http://localhost:5000
pause
