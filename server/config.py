

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:01cs0qxcl5k!@kbj-firstdb.cu8i1dwdnvpi.ap-northeast-2.rds.amazonaws.com/mysns"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    AWS_ACCESS_KEY_ID = 'AKIAUGPOH6LYW2UAOU7P'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_S3_BUCKET_NAME = 'python202201kbj'
    JWT_ALGORITHM = 'HS512'
    JWT_SECRET = 'my_strong_key'
    ALIGO_API_KEY = 'i5m8plmyxhcpwfvty29hbzko2zzgi0nq'
    MAILGUN_API_KEY = 'fea70faa6e0b2dff8740427c0b48f05c-7b8c9ba8-41d27327'


class ProductionConfig(Config): #기본설정 그대로
    pass

class TestConfig(Config): #테스팅환경
    TESTING = True

class DebugConfig(Config): #개발모드
    DEBUG = True