import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'clave_por_defecto')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    FLASK_ENV = 'production'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
