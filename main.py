import datetime
import logging
import os
import random
import time
from dotenv import load_dotenv
import scrape_once

load_dotenv()
debug = os.getenv('DEBUG')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# run scraper for a day (to be restarted by cron on the next day
# if starting from 6:00, the following list would result in following times:
# 06:00, 07:31, 08:26, 09:37, 10:24, 11:29, 12:27, 13:30, 15:15, 16:10, 17:21, 18:08, 19:13, 20:11, 21:14, 22:59, 23:54
intervals = (91, 55, 71, 47, 65, 58, 63, 105, 55, 71, 47, 65, 58, 63, 105, 55, 71) * 10
initial_delay = random.randrange(0, 3)
if debug:
    intervals = (0, 1, 1)
    initial_delay = 3


def main():
    wait_until_start()
    logging.info(f"scraping main loop started, initial delay = {initial_delay}s")
    time.sleep(initial_delay)
    for interval in intervals:
        logging.info("scraping started")
        sumlog = scrape_once.run()
        for line in sumlog:
            logging.info(f"Summary: {line}")
        logging.info(f"sleeping {interval*6} s")
        time.sleep(interval * 6)
    logging.info(f"Exiting simplescrape2/main.py")


def wait_until_start():
    while True:
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(int(os.getenv('START_HOUR')), int(os.getenv('START_MINUTE')))
        logging.info(f"Waiting for {start_time}.")
        if current_time >= start_time:
            break
        else:
            time.sleep(60)

    logging.debug(f"It's {start_time}! Continue with {len(intervals)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
