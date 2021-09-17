class Strategy1:
    """Find today's MACD bullish crossover stocks with RSI between 60 and 80
    Also calculate number of days since the last bearish crossover
    Also put RSI in the response"""
    def __init__(self, company):
        self.stock_name = company.symbol
        self.macd_diff = company.macd_diff
        self.rsi = company.rsi

    def strategy1(self):
        stock_name = self.stock_name
        macd_diff = self.macd_diff
        rsi = self.rsi

        last_macd_diff = macd_diff[-1]
        second_last_macd_diff = macd_diff[-2]

        macd_bullish_crossover = False

        if last_macd_diff > 0 and second_last_macd_diff < 0:
            macd_bullish_crossover = True

        if not macd_bullish_crossover:
            return

        if rsi[-1] < 60 or rsi[-1] > 80:
            return

        last_positive_macd_diff_date = -1
        for i in range(0, len(macd_diff) - 1):
            if macd_diff[i] > 0:
                last_positive_macd_diff_date = i

        days_since_bearish_crossover = len(macd_diff) - last_positive_macd_diff_date - 2

        response = {
            "stock_name": stock_name,
            "days_since_bearish_crossover": days_since_bearish_crossover,
            "rsi": rsi[-1]
        }
        return response


class Strategy2:
    """Find yesterday's MACD bullish crossover stocks with RSI between 60 and 80
    Also calculate number of days since the last bearish crossover
    Check if the MACD diff increased today from yesterday
    Also put RSI in the response"""
    def __init__(self, company):
        self.stock_name = company.symbol
        self.macd_diff = company.macd_diff
        self.rsi = company.rsi

    def strategy2(self):
        stock_name = self.stock_name
        macd_diff = self.macd_diff
        if stock_name=='BCG':
            print(macd_diff)
        rsi = self.rsi

        last_macd_diff = macd_diff[-1]
        second_last_macd_diff = macd_diff[-2]
        third_last_macd_diff = macd_diff[-3]

        yesterday_macd_bullish_crossover = False

        if second_last_macd_diff > 0 and third_last_macd_diff < 0:
            yesterday_macd_bullish_crossover = True

        if not yesterday_macd_bullish_crossover:
            return

        if rsi[-1] < 60 or rsi[-1] > 80:
            return

        if last_macd_diff < second_last_macd_diff:
            return

        last_positive_macd_diff_date = -1
        for i in range(0, len(macd_diff) - 2):
            if macd_diff[i] > 0:
                last_positive_macd_diff_date = i

        days_since_bearish_crossover = len(macd_diff) - last_positive_macd_diff_date - 3

        response = {
            "stock_name": stock_name,
            "days_since_bearish_crossover": days_since_bearish_crossover,
            "rsi": rsi[-1]
        }
        return response
