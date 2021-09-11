# -*- coding: utf-8 -*-
from unittest import TestCase

from technical_indicators_calculator import set_technical_indicators, Company
from technical_indicators_chart_plotting import TechnicalIndicatorsChartPlotter
import yfinance as yf
import pandas as pd

class TestTechnicalIndicator(TestCase):

    def test_tech_indicator(self):
        company = Company('TWTR')
        config = {}
        company.prices = yf.Ticker(company.symbol).history(period='1y')['Close']
        set_technical_indicators(config, company)
        print(company.prices)
        print(company.technical_indicators)
        tacp = TechnicalIndicatorsChartPlotter()
        # tacp.plot_macd(company)
        # tacp.plot_rsi(company)
        # tacp.plot_bollinger_bands(company)


x = TestTechnicalIndicator()
x.test_tech_indicator()
