'''
obtain and filter a list of urls that are contained in an JSON object

DOES NOT WORK - Javascript is loading JSON sdynamically -> use selenium instead
'''

import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path


scraping_target_url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
detail_links_regex = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')

response = requests.get(scraping_target_url, headers=headers)
scraping_target_html = response.text
soup = BeautifulSoup(scraping_target_html, "html.parser")
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

x = Path('../results/bs4.html')
x.write_text(scraping_target_html)
