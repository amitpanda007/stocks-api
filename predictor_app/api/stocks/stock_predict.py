import logging
import datetime as dt
from datetime import timedelta
import json

import requests
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
from predictor_app.settings import ALPHA_VANTAGE_API_KEY
log = logging.getLogger(__name__)
ns = api.namespace('stocks', description='Operations related to Stocks')


def get_stock_symbol(search_text):
    api_url = 'https://www.alphavantage.co/query?'
    _url = f'{api_url}function=SYMBOL_SEARCH&keywords={search_text}&apikey={ALPHA_VANTAGE_API_KEY}'
    resp = requests.get(_url).json()
    try:
        stock_symbols_list = resp['bestMatches']
        for item in stock_symbols_list:
            if 'India' in item['4. region']:
                # print(item)
                return item['1. symbol'], item['2. name']
    except KeyError:
        print("Error happened while parsing response of stock symbol search")
    return '',''


@ns.route("/av/search/<stock_name>")
class StockAlphaVantageSearch(Resource):
    """
    Get Company stocks for last 100 days with a provided stock symbol for Alpha Vantage
    """
    def get(self, stock_name):
        # find symbol from https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=state%20bank%20of%20india&apikey=RDHWB3SUU8YDH8C2
        # stock_symbol = 'BSE:500570' This is for TTM
        api_url = 'https://www.alphavantage.co/query?'
        print(get_stock_symbol(stock_name))
        stock_symbol, stock_name = get_stock_symbol(stock_name)
        if stock_symbol == '' or stock_name == '':
            return {'errorCode': 50001, 'message': 'Unable to find Stocks with the search name provided.'}

        _url = f'{api_url}function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
        resp = requests.get(_url).json()
        resp['Meta Data']['6. Name'] = stock_name
        return resp


@ns.route("/av/<stock_symbol>")
class StockAlphaVantage(Resource):
    """
    Get Company stocks for last 100 days with a provided stock symbol for Alpha Vantage
    """
    def get(self, stock_symbol):
        # find symbol from https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=state%20bank%20of%20india&apikey=RDHWB3SUU8YDH8C2
        # stock_symbol = 'BSE:500570' This is for TTM
        api_url = 'https://www.alphavantage.co/query?'
        _url = f'{api_url}function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
        resp = requests.get(_url)
        return resp.json()


@ns.route("/<company_id>/<days>")
class StockNumDays(Resource):
    """
    Get Company stocks for number of days provided
    """

    def get(self, company_id, days):
        # quandl_api_key = 'yLkpXUMtXk-WXgkobvoo'
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

