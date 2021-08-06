from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
from test import TitleSearcher
from stockanalysis import TextAnalyzer
import io
import time
import pandas as pd
from detectionSupport import detectionSupport;

# stockLink = 'https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o1000,sh_price_o5,sh_short_o15,ta_perf_13w10o,ta_perf2_1wdown&ft=4'
stockLink = 'https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o1000,sh_price_o5,sh_short_high,ta_perf_13w10o,ta_perf2_4wdown&ft=4'
root = 'https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o1000,sh_price_o5,sh_short_o15,ta_perf_13w10o,ta_perf2_4wdown&ft=4'

dfTwo = io.open("excel/" + 'finalResult.csv', "a")
dfTwo.write("{}, {}, {}, {} \n".format('stock', 'positive', 'neutral', 'negative'))
dfTwo.close()

class stockPick:
    routingNum = 0;
    def mainFunction(link):
        req = Request(link, headers={"User-Agent": 'Mozilla/5.0'})
        stockRead = urlopen(req).read()
        with requests.Session() as c:
            soup = BeautifulSoup(stockRead, 'html5lib')
            # print(soup)

            for item in soup.find_all('a', attrs={'class': 'screener-link-primary'}):
                # item = item.split('p=d&amp')[1]
                document = io.open("excel/" + item.get_text() + ".csv", "a")

                document.write("{}, {}, {}, {} \n".format('title', 'time', 'description', 'link'))
                document.close()
                print(item.get_text())
                TitleSearcher.news(item.get_text(), item.get_text())
                TextAnalyzer.positiveNegativeNeutralStock(item.get_text())
                time.sleep(2)

            next = soup.find('b', text='next')
            # print(next)
            if next != None:
                stockPick.routingNum += 1;
                #next = (next['href'])
                link = root + '&r='+str(((20 * stockPick.routingNum) + 1))
                stockPick.mainFunction(link)
            # TitleSearcher.news(link, csvFile)
        # dfThree = pd.read_csv("excel/finalResult.csv", names=['stock', 'positive', 'neutral', 'negative'])

#dfThree = pd.read_csv("excel/finalResult.csv", names=['stock', 'positive', 'neutral', 'negative'])
#df1 = dfThree.sort_values(by=['positive'], ascending=False, ).head(3)
stockPick.mainFunction(root)
dfThree = pd.read_csv("excel/finalResult.csv", names=['stock', 'positive', 'neutral', 'negative'])
df1 = dfThree.sort_values(by=['positive'], ascending=False, ).head(5)
for val in df1['stock'].tolist():
    if val != 'stock':
        print(val)
        detectionSupport.supportPivotPoints(val)

    # dfThree = pd.read_csv("excel/finalResult.csv", names=['stock', 'positive', 'neutral', 'negative'])
    # df1 = dfThree.sort_values(by=['positive'], ascending=False, ).head(3)
    # for val in df1['stock'].tolist():
    # if val !='stock':
    # print(val)
    # detectionSupport.supportPivotPoints(val)
