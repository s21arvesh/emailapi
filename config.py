class config(object):
    MAIL_PORT = '587'


class ProductionConfig(config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    TESTING = False
    DB_SERVER = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'detox_db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'sarvesh21'

class TestingConfig(config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
