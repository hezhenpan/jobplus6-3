class BaseConfig(object):
    SECRET_KEY = 'maybe nobady care'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost:3306/jobplus?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    INDEX_PER_PAGE = 9
    COMINFO_PER_PAGE = 9
    ADMIN_PER_PAGE = 10


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
