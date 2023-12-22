import re
import time
from bs4 import BeautifulSoup, SoupStrainer
from lxml import html
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

#x = Path('./results/scratch.json')
detail_links_regex = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')
#detail_links_regex = re.compile(r'mietwohnungen/wien')
url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"


class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

#This does the magic.Loads everything
r = Render(url)
#result is a QString.
result = r.frame.toHtml()
formatted_result = str(result.toAscii())
tree = html.fromstring(driver.page_source)
archive_links = tree.xpath('//a/@href')
print(archive_links)

#soup = BeautifulSoup(driver.page_source, "html.parser")
#for link in soup.find_all("a"):
#    href = link.get("href")
#    if href and re.search(detail_links_regex, href):
#        print(f"+ {href}")
    #else:
    #    print(f"- {href}")
pass







# requests-html
#session = HTMLSession()
#r = session.get(scraping_target_url)
#print(r.html.links)






#for link in BeautifulSoup(x.read_text(), "html.parser", parse_only=SoupStrainer('a', href=True)):
#    print(link['href'])


#html = x.read_text()
#regex = re.compile(r'<<a.*?>(.*?)</a>')
#results = regex.findall(html, re.DOTALL)
#print(results)