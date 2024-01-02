from QiDataProcessing.Core.TradingDayHelper import TradingDayHelper
import datetime


day = TradingDayHelper.get_pre_trading_day(datetime.datetime(2023, 1, 4))
print(day)
