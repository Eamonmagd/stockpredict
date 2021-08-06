from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = Request("https://www.equities.com/news/atara-biotherapeutics-inc-atra-soars-4-9-on-february-05/", headers={"User-Agent": 'Mozilla/5.0'})
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")


# kill all script and style elements
for script in soup(["script", "style", "header"]):
    script.extract()    # rip it out
# for p in soup.find_all("p"):
#     print (p.text)
# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = ''.join(chunk for chunk in chunks if chunk)
# text = '\n'.join(chunk for chunk in chunks if chunk)
print(text)
#
# regex = re.compile('.*footer.*')
# stop_at =  soup.find("div", {"class" : regex})
# for script in soup(["script", "style", "header"]):
#     script.extract()    # rip it out
# for p in soup.find_all("p"):
#     print (p.text)
for script in soup(["script", "style", "header"]):
    script.extract()    # rip it out
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = ''.join(chunk for chunk in chunks if chunk)
print(text)