import json
import os
import re
import time
import warnings
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

warnings.simplefilter("ignore", ResourceWarning)
load_dotenv()

# Willhaben parameter
scraping_target_host = "https://www.willhaben.at"
scraping_target_path = os.getenv('SCRAPING_TARGET_PATH')
filter_detail_link = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')

class ScrapeWillhaben:
    def __init__(self):
        pass

    def scrape(self) -> list:
        # test values:
        # detail_links_regex = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')
        assert scraping_target_host[-1:] != '/'
        assert scraping_target_path[0:1] == '/'
        scraping_target_url = scraping_target_host + scraping_target_path

        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-agent={my_user_agent}")
        options.add_argument("--headless")
        options.page_load_strategy = "none"  # we don't need it as the page is populated with dynamic JavaScript code
        driver = Chrome(options=options)
        # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
        driver.implicitly_wait(10)
        driver.get(scraping_target_url)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(5)

        #tree = html.fromstring(driver.page_source)
        #archive_links = tree.xpath('//a/@href')

        soup = BeautifulSoup(driver.page_source, "html.parser")
        result = []
        for script in soup.find_all("script"):
            try:
                assert script.attrs['type'] == 'application/ld+json'
                script_contents = script.string
                item_container = json.loads(script_contents)
                if item_container['@type'] == 'ItemList':
                    for list_item in item_container['itemListElement']:
                        result.append(f"{scraping_target_host}{list_item['url']}")
            except Exception:
                pass
        return result


if __name__ == "__main__":
    print('starting')
    scraping_target_host = "https://www.willhaben.at"
    scraping_target_path = "/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
    filter_detail_link = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')

    scraper = ScrapeWillhaben()
    result = scraper.scrape(scraping_target_host, scraping_target_path, filter_detail_link)
    print('done')
    print('\n'.join(result))
