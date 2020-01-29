# configuration

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'ssbautomator888'
    USERNAME = None
    PASSWORD = None

    DBTYPE = 'sqlite'
    SQL_FILE = "databases/main.sqlite"

    # web configurations
    UI_TITLE = "SSB Automator"
    UI_ICONTITLE1 = "SSB"
    UI_ICONTITLE2 = "Automator"
    UI_MINITITLE1 = "S"
    UI_MINITITLE2 = "A"

    APP_PORT = 5000
    API_URL = 'http://localhost:%d' % APP_PORT
    AMQP_HOST = "localhost"


class ProductionConfig(Config):
    DEBUG = False
    RQ_HOST = "localhost"
    RQ_PORT = "6379"
    RQ_QUEUENAME = "ssbautomator"

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
