from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import io
import time as tm
root = "https://www.google.com/"
stockPick = "ayro"
link = "https://www.google.co.uk/search?q="+stockPick+"+stock&newwindow=1&safe=off&hl=en&tbm=nws&sxsrf=ALeKk03BUjzC0aBuJvxwt7PjB-xUZq3ruQ:1612787760455&source=lnt&tbs=qdr:w&sa=X&ved=0ahUKEwjK57zMptruAhWZh1wKHQEfD9oQpwUIKQ&biw=1920&bih=937&dpr=1"

class TitleSearcher:
    def news(link, csvFile):
        if  "http" in link:
            link = link
        else:
            link = "https://www.google.co.uk/search?q=" + link + "+stock&newwindow=1&safe=off&hl=en&tbm=nws&sxsrf=ALeKk03BUjzC0aBuJvxwt7PjB-xUZq3ruQ:1612787760455&source=lnt&tbs=qdr:w&sa=X&ved=0ahUKEwjK57zMptruAhWZh1wKHQEfD9oQpwUIKQ&biw=1920&bih=937&dpr=1"

        req = Request(link, headers={"User-Agent": 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        with requests.Session() as c:
            soup = BeautifulSoup(webpage, 'html5lib')
            # print(soup)
            soup.encode("utf-8")
            for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
                # print(item)

                try:
                    #tm.sleep(1)
                    raw_link = (item.find('a', href=True)['href'])
                    link = (raw_link.split("/url?q=")[1]).split("&sa=U&")[0]

                    title = item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text()
                    title = title.replace(",", "")
                    description = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
                    description = description.replace(",", "")
                    time = description.split(" · ")[0]
                    descript = description.split(" · ")[1]
                    #print(title)
                    #print(time)
                    #print(descript)
                    #print(link)

                    req = Request(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                    stockRead = urlopen(req, timeout=10).read()

                    #print(link)
                    soup = BeautifulSoup(stockRead, 'html5lib')
                    for script in soup(["script", "style", "header"]):
                        script.extract()  # rip it out
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ''.join(chunk for chunk in chunks if chunk)
                    final = (descript+text)
                    final = final.replace(",", "")
                    #final = descript
                    document = io.open("excel/"+csvFile+".csv", "a")
                    document.write("{}, {}, {}, {} \n".format(title.encode("utf-8"), time.encode("utf-8"), final.encode("utf-8"), link.encode("utf-8")))
                    document.close()
                except:
                    #print('problem')
                    try:
                        document = io.open("excel/"+csvFile+".csv", "a")
                        document.write("{}, {}, {}, {} \n".format(title.encode("utf-8"), time.encode("utf-8"), descript.encode("utf-8"), link.encode("utf-8")))
                        document.close()
                    except:
                        print("problem with downloading data")
            next = soup.find('a', attrs={'aria-label': 'Next page'})
            #print(next)
            if next!= None:
                next = (next['href'])
                link = root + next
                TitleSearcher.news(link, csvFile)


