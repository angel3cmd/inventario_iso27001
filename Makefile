init:
    pip install -r requirements.txt
    python -c "from cryptography.fernet import Fernet; open('secret.key', 'wb').write(Fernet.generate_key())"
    python init_db.py

run:
    docker compose up -d

reset:
    docker compose down
    docker compose build
    docker compose up -d

clean:
    rm -f secret.key
    rm -f auditoria_backups.csv auditoria_backups.pdf
