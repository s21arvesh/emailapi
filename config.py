class config(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USERNAME = 'sarveshmestry01@gmail.com'
    MAIL_PASSWORD = 'cvve orel jpnu sfwe'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'no-reply@gmail.com'


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

    API_JSON_SCHEMA = 'src/include/api_json_schemas.json'
    DEFAULT_SENDER = 'no-reply@gmail.com'
class TestingConfig(config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
