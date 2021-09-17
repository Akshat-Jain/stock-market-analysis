# -*- coding: utf-8 -*-
import time
from datetime import timedelta

import pandas as pd
import schedule
import yfinance as yf
from nsepy import get_history

from strategies import *
from technical_indicators_calculator import *
from ticker_symbols import *
from utils import date_util, mail_util


def get_data_for_stock(stock_name):
    historical_data = get_history(symbol=stock_name,
                                  start=date_util.getLastDate() - timedelta(days=365),
                                  end=date_util.getLastDate())

    try:
        historical_data_yfinance = yf.Ticker(stock_name + ".NS").history(
            start=date_util.getLastDate() - timedelta(days=365))
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print("Decoding JSON has failed")

    if historical_data_yfinance.empty:
        print("Incorrect symbol: ", stock_name)
        return None

    historical_data_yfinance['Date'] = historical_data_yfinance.index
    historical_data_yfinance = pd.DataFrame(historical_data_yfinance, columns=['Date', 'Close'])

    closing_prices = pd.Series(historical_data_yfinance['Close'], index=historical_data_yfinance.index)

    company = Company(stock_name)
    company.prices = closing_prices
    company.technical_indicators = pd.DataFrame()
    company.technical_indicators['Close'] = closing_prices

    # tacp = TechnicalIndicatorsChartPlotter()
    # tacp.plot_macd(company)
    # tacp.plot_rsi(company)
    # tacp.plot_bollinger_bands(company)

    macd_diff = get_macd(company)
    rsi = get_rsi(company)

    company.macd_diff = macd_diff
    company.rsi = rsi
    return company


def analyse_stocks():
    companies = []

    # for stock_name in ["TEJASNET"]:
    for stock_name in nseTop1000MarketCap:
        print(stock_name, flush=True)
        company = get_data_for_stock(stock_name)

        if company is None:
            continue

        macd_diff = company.macd_diff
        rsi = company.rsi

        if macd_diff is None:
            continue

        if macd_diff.index[-1].date() != date_util.getLastDate():
            # This doesn't work when last day was holiday.
            # Todo: Check later: print(nsepy.live.getworkingdays(getLastDate() - timedelta(days=365), getLastDate()))
            continue

        if len(macd_diff) < 2:
            print("Macd_diff length is less than 2")
            continue

        companies.append(company)

    strategy1_response_list = []
    strategy2_response_list = []
    for company in companies:
        stock_name = company.symbol
        macd_diff = company.macd_diff
        rsi = company.rsi

        strategy_1 = Strategy1(company)
        strategy1_response = strategy_1.strategy1()
        if strategy1_response is not None:
            strategy1_response_list.append(strategy1_response)

        if len(macd_diff) < 3:
            continue

        strategy_2 = Strategy2(company)
        strategy2_response = strategy_2.strategy2()
        if strategy2_response is not None:
            strategy2_response_list.append(strategy2_response)

    strategy1_response_list.sort(key=lambda x: x["days_since_bearish_crossover"], reverse=True)
    strategy2_response_list.sort(key=lambda x: x["days_since_bearish_crossover"], reverse=True)

    print(strategy1_response_list)
    print(strategy2_response_list)

    mail_util.create_and_send_mail(strategy1_response_list, 'Strategy 1')
    mail_util.create_and_send_mail(strategy2_response_list, 'Strategy 2')


# Schedule everyday at 12:30 PM UTC, that is 6 PM IST
schedule.every().day.at("12:30").do(analyse_stocks)

while True:
    schedule.run_pending()
    time.sleep(60)
