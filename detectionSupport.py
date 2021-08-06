import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

yf.pdr_override()

now = dt.datetime.now()

start = dt.date.today() - relativedelta(months=5)


class detectionSupport:
    def supportPivotPoints(stock):
        print(stock)
        df = pdr.get_data_yahoo(stock, start, now)
        df["High"].plot(label="high")
        pivots = []
        dates = []
        counter = 0
        lastPivot = 0
        Range = [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]
        dateRange = [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 1000000]
        #        Range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in df.index:
            currentMax = min(Range, default=0)
            value = round(df["High"][i], 2)
            Range = Range[1:9]
            Range.append(value)
            dateRange = dateRange[1:9]
            dateRange.append(i)
            if currentMax == min(Range, default=0):
                counter += 1
            else:
                counter = 0
            if counter == 5:
                lastPivot = currentMax
                dateLoc = Range.index(lastPivot)
                lastDate = dateRange[dateLoc]
                pivots.append(lastPivot)
                dates.append(lastDate)
        # print(str(pivots))
        # print(str(dates))
        timeD = dt.timedelta(days=30)
        for index in range(len(pivots)):
            print(str(pivots[index]) + ": " + str(dates[index]))
            plt.plot_date([dates[index], dates[index] + timeD],
                          [pivots[index], pivots[index]], linestyle="-", linewidth=2, marker=",")
        plt.show()


#dfThree = pd.read_csv("excel/finalResult.csv", names=['stock', 'positive', 'neutral', 'negative'])
#df1 = dfThree.sort_values(by=['positive'], ascending=False, ).head(5)
#for val in df1['stock'].tolist():
#    if val !='stock':
#        print(val)
#        detectionSupport.supportPivotPoints(val)
