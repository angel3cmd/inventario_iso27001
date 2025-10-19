import os

class Config:
    # 🔐 Clave secreta para sesiones Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'clave_por_defecto')

    # 🗂️ Rutas configurables
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'inventario.db')
    BACKUP_FOLDER = os.getenv('BACKUP_FOLDER', 'backups')
    SECRET_KEY_PATH = os.getenv('SECRET_KEY_PATH', 'secret.key')

    # ⚙️ Configuración general
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
