import logging.config

import os
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from predictor_app import settings
from predictor_app.api.stocks.stock_predict import ns as stock_predict_namespace
from predictor_app.api.restplus import api
from predictor_app.task_queue.celery_config import celery, init_celery
from predictor_app.database import db, init_database, reset_database

app = Flask(__name__)
###############################
# Logging configuration section
###############################
# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
# logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

##################################
# Web Token configuration section
##################################
jwt = JWTManager(app)

#####################################
# Celery tasks configuration section
#####################################
# celery = make_celery(app)

####################################################################################
# CORS configuration section
# spefic usgae for path : cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
####################################################################################
CORS(app)


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI_MYSQL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    flask_app.config["CELERY_BROKER_URL"] = settings.CELERY_BROKER_URL
    flask_app.config["CELERY_RESULT_BACKEND"] = settings.CELERY_RESULT_BACKEND


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api-v1', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(stock_predict_namespace)
    flask_app.register_blueprint(blueprint)

    init_celery(celery, flask_app)

    db.init_app(flask_app)
    # reset_database(flask_app)
    with flask_app.app_context():
        db.create_all()
    print("App Initialization Complete!")


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()