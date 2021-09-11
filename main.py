# TODO: USE YFINANCE LIBRARY TO FETCH STOCK PRICES
# https://www.youtube.com/watch?v=HmgmhOpS42A

# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

import nsepy.nselist
from nsepy import get_history  # https://nsepy.xyz/
import pandas as pd
import numpy as np

from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from ticker_symbols import *

from technical_indicators_chart_plotting import TechnicalIndicatorsChartPlotter
from utils import *
from strategies import *

stocksToBuy = []

import yfinance as yf

# msft = yf.Ticker("PRAJIND.NS")
#
# # get stock info
# print(msft.history())
#
# # get historical market data
# hist = msft.history(period="max")
# print(type(hist))
#
# # show actions (dividends, splits)
# print(hist)

class Company:
    def __init__(self, symbol):
        self.symbol = symbol
        self.technical_indicators = None
        self.prices = None


# def set_technical_indicators(company):
#     company.technical_indicators = pd.DataFrame()
#     company.technical_indicators['Close'] = company.prices

def generate_buy_sell_signals(condition_buy, condition_sell, dataframe, strategy):
    last_signal = None
    indicators = []
    buy = []
    sell = []
    for i in range(0, len(dataframe)):
        # if buy condition is true and last signal was not Buy
        if condition_buy(i, dataframe) and last_signal != 'Buy':
            last_signal = 'Buy'
            indicators.append(last_signal)
            buy.append(dataframe['Close'].iloc[i])
            sell.append(np.nan)
        # if sell condition is true and last signal was Buy
        elif condition_sell(i, dataframe) and last_signal == 'Buy':
            last_signal = 'Sell'
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(dataframe['Close'].iloc[i])
        else:
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(np.nan)

    dataframe[f'{strategy}_Last_Signal'] = np.array(last_signal)
    dataframe[f'{strategy}_Indicator'] = np.array(indicators)
    dataframe[f'{strategy}_Buy'] = np.array(buy)
    dataframe[f'{strategy}_Sell'] = np.array(sell)


def get_macd(company):
    close_prices = company.prices
    dataframe = company.technical_indicators
    window_slow = 26
    signal = 9
    window_fast = 12
    macd = MACD(company.prices, window_slow, window_fast, signal)

    dataframe['MACD'] = macd.macd()
    dataframe['MACD_Histogram'] = macd.macd_diff()
    dataframe['MACD_Signal'] = macd.macd_signal()

    # generate_buy_sell_signals(
    #     lambda x, dataframe: dataframe['MACD'].values[x] < dataframe['MACD_Signal'].iloc[x],
    #     lambda x, dataframe: dataframe['MACD'].values[x] > dataframe['MACD_Signal'].iloc[x],
    #     dataframe,
    #     'MACD')
    # return dataframe
    return macd.macd_diff()


def get_rsi(company):
    close_prices = company.prices
    dataframe = company.technical_indicators
    rsi_time_period = 14

    rsi_indicator = RSIIndicator(close_prices, rsi_time_period)
    dataframe['RSI'] = rsi_indicator.rsi()
    # print(rsi_indicator.rsi())

    low_rsi = 40
    high_rsi = 60

    # generate_buy_sell_signals(
    #     lambda x, dataframe: dataframe['RSI'].values[x] < low_rsi,
    #     lambda x, dataframe: dataframe['RSI'].values[x] > high_rsi,
    # dataframe, 'RSI')

    # return dataframe
    return rsi_indicator.rsi()


def get_bollinger_bands(company):
    close_prices = company.prices
    dataframe = company.technical_indicators

    window = 20

    indicator_bb = BollingerBands(close=close_prices, window=window, window_dev=2)

    # Add Bollinger Bands features
    dataframe['Bollinger_Bands_Middle'] = indicator_bb.bollinger_mavg()
    dataframe['Bollinger_Bands_Upper'] = indicator_bb.bollinger_hband()
    dataframe['Bollinger_Bands_Lower'] = indicator_bb.bollinger_lband()

    # generate_buy_sell_signals(
    #     lambda x, signal: signal['Close'].values[x] < signal['Bollinger_Bands_Lower'].values[x],
    #     lambda x, signal: signal['Close'].values[x] > signal['Bollinger_Bands_Upper'].values[x],
    #     dataframe, 'Bollinger_Bands')

    return dataframe


def checkStock(stock_name, macd_diff, rsi):
    stocksToBuy.append({
        "stock_name": stock_name,
        "macd_diff": macd_diff,
        "rsi": rsi
    })
    return

def getDataForStock(stock_name):
    historical_data = get_history(symbol=stock_name,
                       start=getLastDate() - timedelta(days=365),
                       end=getLastDate())

    try:
        historical_data_yfinance = yf.Ticker(stock_name + ".NS").history(start=getLastDate() - timedelta(days=365))
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print("Decoding JSON has failed")

    # print(historical_data)
    # print(historical_data_yfinance)

    # if historical_data.empty:
    #     # print("Incorrect symbol: ", stock_name)
    #     return None, None

    if historical_data_yfinance.empty:
        print("Incorrect symbol: ", stock_name)
        return None, None

    # print(historical_data)

    # historical_data['Date'] = historical_data.index
    # historical_data = pd.DataFrame(historical_data, columns=['Date', 'Close'])

    historical_data_yfinance['Date'] = historical_data_yfinance.index
    historical_data_yfinance = pd.DataFrame(historical_data_yfinance, columns=['Date', 'Close'])

    # closing_prices = pd.Series(historical_data['Close'], index=historical_data.index)
    closing_prices = pd.Series(historical_data_yfinance['Close'], index=historical_data_yfinance.index)

    company = Company(stock_name)
    company.prices = closing_prices
    company.technical_indicators = pd.DataFrame()
    company.technical_indicators['Close'] = closing_prices

    # get_macd(company)
    # get_rsi(company)
    # get_bollinger_bands(company)

    # print()
    # print(company)
    # print(company.prices)
    # print(company.technical_indicators)

    tacp = TechnicalIndicatorsChartPlotter()
    # tacp.plot_macd(company)
    # tacp.plot_rsi(company)
    # tacp.plot_bollinger_bands(company)



    # latestDate = getLastDate()
    # print(latestDate)
    # for x in range(0, 10):
    #   previousDate = getPreviousDate(latestDate)
    #   print(previousDate)
    #   latestDate = previousDate

    # print("Fetching data")
    macd_diff = get_macd(company)
    rsi = get_rsi(company)

    # print("stock_name", stock_name)
    # print("macd_diff", macd_diff)
    # print("rsi", rsi)
    # print()
    # print()

    # checkStock(stock_name, macd_diff, rsi)
    return macd_diff, rsi

    # print("Successful")
    # print(macd_diff)
    # print(rsi)

# print(nseTop1000MarketCap)

strategy1_response_list = []

# print(getLastDate())

for stock_name in nseTop1000MarketCap:
# for stock_name in ["TEJASNET"]:
    print(stock_name)
    macd_diff, rsi = getDataForStock(stock_name)
    # print(macd_diff)
    # print(rsi)

    if macd_diff is None:
        continue

    if macd_diff.index[-1].date() != getLastDate():
        # todo: this doesn't work when last day was holiday
        # print(stock_name, macd_diff.index[-1])
        continue

    if len(macd_diff) < 2:
        print("Macd_diff length is less than 2")
        continue

    strategy1_response = strategy1(stock_name, macd_diff, rsi)
    if strategy1_response is None:
        continue
    else:
        # print(stock_name)
        strategy1_response_list.append(strategy1_response)
    # break

strategy1_response_list.sort(key=lambda x: x["days_since_bearish_crossover"], reverse=True)
print(strategy1_response_list)

# print(stocksToBuy)
# print(nsepy.live.getworkingdays(getLastDate() - timedelta(days=365), getLastDate()))
