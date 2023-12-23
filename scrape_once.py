import json
import re
from datetime import datetime
from pathlib import Path
from typing import List

from scrape_willhaben import ScrapeWillhaben

# Willhaben parameter
scraping_target_host = "https://www.willhaben.at"
scraping_target_path = "/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
filter_detail_link = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')
# Configuration
Path('./results/').mkdir(exist_ok=True)
prev_links_path = Path('./results/links_prev.json')
new_links_path = Path('./results/newurls.txt')
logbook_path = Path('./results/logbook.txt')


def run() -> list:
    links_prev = load_detail_items_previous_run()
    links_now = scrape_detail_links_from_target()
    save_links(links_now)
    new_urls = diff_links_not_in_prev(links_now, links_prev)
    new_links_path.write_text('\n'.join(new_urls))
    log_new(new_urls)
    sum_log: list[str] = [str]
    sum_log.append(f"{len(links_prev)} previous and {len(links_now)} current links found")
    if len(new_urls):
        sum_log += new_urls
    else:
        sum_log.append('no new urls found')
    return sum_log


def load_detail_items_previous_run() -> list:
    try:
        with Path.open(prev_links_path) as fd:
            return json.load(fd)
    except Exception:
        return []


def scrape_detail_links_from_target() -> list:
    scraper = ScrapeWillhaben()
    return scraper.scrape(scraping_target_host, scraping_target_path, filter_detail_link)


def diff_links_not_in_prev(links_now: list, links_prev: list) -> list:
    new_urls = []
    for url in links_now:
        if url not in links_prev:
            new_urls.append(url)
    return new_urls


def save_links(links_now: list):
    with Path.open(prev_links_path, 'w') as fd:
        return json.dump(links_now, fd)


def log_new(new_urls):
    Path(logbook_path).touch()
    now = datetime.now().isoformat(timespec='minutes')
    with open(logbook_path, 'a', newline='') as fd:
        for url_path in new_urls:
            fd.write(f"{now} {url_path} \n")


# simple test
if __name__ == "__main__":
    run(scraping_target_host, scraping_target_path, filter_detail_link)