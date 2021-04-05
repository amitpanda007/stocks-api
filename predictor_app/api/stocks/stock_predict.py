import logging
import datetime as dt
from datetime import timedelta

from flask import request
try:
    from flask_restplus import Resource, Api
except ImportError:
    import werkzeug
    werkzeug.cached_property = werkzeug.utils.cached_property
    from flask_restplus import Resource, Api
from flask_jwt_extended import create_access_token
from predictor_app.api.restplus import api
import pandas_datareader as stocks

log = logging.getLogger(__name__)
ns = api.namespace('stocks', description='Operations related to Stocks')


@ns.route("/<company_id>")
class CurrentStock(Resource):
    """
    Get Company stocks for today
    """

    def get(self, company_id):
        data = stocks.DataReader(company_id, 'yahoo', start=dt.datetime(2021, 4, 1), end=dt.datetime(2021, 4, 1))


@ns.route("/<company_id>/<days>")
class CurrentStock(Resource):
    """
    Get Company stocks for number of days provided
    """

    def get(self, company_id, days):
        today = dt.datetime.today()
        cur_year = today.year
        cur_month = today.month
        cur_day = today.day
        end =  dt.datetime(cur_year, cur_month, cur_day)

        old_date = dt.datetime.today() - timedelta(days=int(days))
        old_year = old_date.year
        old_month = old_date.month
        old_day = old_date.day
        start = dt.datetime(old_year, old_month, old_day)

        data = stocks.DataReader(company_id, 'yahoo', start, end)
        print(data)


@ns.route("/predict")
class Predict(Resource):
    """
    Predict stock price for the next day
    """

    def get(self):
        return {"message": "Route Works"}

    @api.doc(params={'test': 'Test test'})
    def post(self):
        return {"message": "Route Works"}

