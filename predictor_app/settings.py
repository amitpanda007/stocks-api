# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_SERVER_HOST = '0.0.0.0'
FLASK_SERVER_PORT = '5000'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
# SQLALCHEMY_DATABASE_URI_MYSQL = 'mysql+mysqldb://root:Pa55word@127.0.0.1:3306/stocks'
SQLALCHEMY_DATABASE_URI_MYSQL = 'mysql+mysqldb://root:Pa55word@192.168.100.117:3306/stocks'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# MySQL settings
MYSQL_HOST ='192.168.100.117'
# MYSQL_HOST ='127.0.0.1'
MYSQL_DATABASE ='stocks'
MYSQL_USER ='root'
MYSQL_PASSWORD = 'Pa55word'

# JWT setting
JWT_SECRET_KEY = 'super-secret' # change in production

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = 'RDHWB3SUU8YDH8C2'


#Celery config
CELERY_BROKER_URL = 'redis://13.234.20.129:6379'
CELERY_RESULT_BACKEND = 'redis://13.234.20.129:6379'
