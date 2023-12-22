import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


# scraping_target_url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
scraping_target_url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
relevant_urls_prev_path = Path('./results/relevant_urls_prev.json')
newurls_path = Path('./results/newurls.txt')
logbook_path = Path('./results/logbook.txt')
detail_links_regex = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')


def main():
    links = scrape_all_links_from_target()
    relevant_urls_now = reduce_to_relevant_urls(links)
    relevant_urls_prev = load_relevant_urls_previous_run()
    save_relevant_urls_now(relevant_urls_now)
    new_urls = relevant_urls_now_minus_prev(relevant_urls_now, relevant_urls_prev)
    write_new_urls(new_urls)


def scrape_all_links_from_target() -> list:
    response = requests.get(scraping_target_url)
    scraping_target_html = response.text
    soup = BeautifulSoup(scraping_target_html, "html.parser")
    return soup.find_all("a")


def reduce_to_relevant_urls(links: list) -> list:
    urls = []
    for link in links:
        href = link.get("href")
        if href and re.search(detail_links_regex, href):
            urls.append(href)
            print(f"+ {href}")
        else:
            print(f"- {href}")
    return urls


def load_relevant_urls_previous_run() -> list:
    try:
        with Path.open(relevant_urls_prev_path) as fd:
            return json.load(fd)
    except Exception:
        return []


def save_relevant_urls_now(relevant_urls_now: list):
    with Path.open(relevant_urls_prev_path, 'w') as fd:
        return json.dump(relevant_urls_now, fd)


def relevant_urls_now_minus_prev(relevant_urls_now: list, relevant_urls_prev: list) -> list:
    new_urls = []
    for now_url in relevant_urls_now:
        if now_url not in relevant_urls_prev:
            new_urls.append(now_url)
    return new_urls


def write_new_urls(new_urls):
    u = urlparse(scraping_target_url)
    host = str(u.scheme + '://' + u.netloc)
    with open(newurls_path, 'w', newline='') as fd:
        for url_path in new_urls:
            fd.write(host + url_path + '\n')


def log_new(new_urls):
    now = datetime.now().isoformat()
    with open(logbook_path, 'a', newline='') as fd:
        for url_path in new_urls:
            fd.write(f"{now} {url_path} \n")


if __name__ == "__main__":
    main()