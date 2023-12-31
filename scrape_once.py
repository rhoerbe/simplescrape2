import json
from datetime import datetime
from pathlib import Path
import send_chatmsg
from scrape_willhaben import ScrapeWillhaben


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
    deliver_new_links(new_urls)
    log_new(new_urls)
    sum_log = []
    if len(new_urls):
        sum_log += new_urls
        sum_log.append(f"scrape_once: {len(new_urls)} new items found")
    else:
        sum_log.append(f"scrape_once: no new items found in {len(links_now)} scraped urls")
    return sum_log


def load_detail_items_previous_run() -> list:
    try:
        with Path.open(prev_links_path) as fd:
            return json.load(fd)
    except Exception:
        return []


def scrape_detail_links_from_target() -> list:
    scraper = ScrapeWillhaben()
    return scraper.scrape()


def diff_links_not_in_prev(links_now: list, links_prev: list) -> list:
    new_urls = []
    for url in links_now:
        if url not in links_prev:
            new_urls.append(url)
    return new_urls


def deliver_new_links(new_urls):
    new_urls_str = '\n'.join(new_urls)
    new_links_path.write_text(new_urls_str)
    if new_urls_str:
        send_chatmsg.main(new_urls_str)


def save_links(links_now: list):
    with Path.open(prev_links_path, 'w') as fd:
        return json.dump(links_now, fd, indent=2)


def log_new(new_urls):
    Path(logbook_path).touch()
    now = datetime.now().isoformat(timespec='minutes')
    with open(logbook_path, 'a', newline='') as fd:
        for url_path in new_urls:
            fd.write(f"{now} {url_path} \n")


# simple test
if __name__ == "__main__":
    run()