from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def decrypt_file(encrypted_path, output_path):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_path, "rb") as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(output_path, "wb") as dec_file:
        dec_file.write(decrypted)

    print(f"Archivo restaurado: {output_path}")
