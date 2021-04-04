import logging

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from predictor_app.api.restplus import api

log = logging.getLogger(__name__)
ns = api.namespace('stocks', description='Operations related to Stocks')


@ns.route("/predict")
class Login(Resource):
    """
    Login user
    """

    def get(self):
        return {"message": "Route Works"}

    @api.doc(params={'test': 'Test test'})
    def post(self):
        return {"message": "Route Works"}

