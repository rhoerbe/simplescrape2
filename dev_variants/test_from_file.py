import json
import re
from bs4 import BeautifulSoup, SoupStrainer
#from lxml import html
from pathlib import Path

detail_links_regex = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')
x = Path('./results/selenium.html')
html = x.read_text()

#tree = html.fromstring(driver.page_source)
#archive_links = tree.xpath('//a/@href')

soup = BeautifulSoup(html, "html.parser")
i = 0
for script in soup.find_all("script"):
    try:
        assert script.attrs['type'] == 'application/ld+json'
        script_contents = script.string
        item_container = json.loads(script_contents)
        if item_container['@type'] == 'ItemList':
            for list_item in item_container['itemListElement']:
                print(list_item['url'])
                i += 1
    except Exception:
        pass
print(i)

