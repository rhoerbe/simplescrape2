import random
import time
import scrape_once


def main():
    # run scraper for a day (to be restarted by cron on the next day
    # starting from 6:00, the following list would result in
    # 06:00, 07:31, 08:26, 09:37, 10:24, 11:29, 12:27, 13:30, 15:15, 16:10, 17:21, 18:08, 19:13, 20:11, 21:14, 22:59, 23:54
    intervals = (91, 55, 71, 47, 65, 58, 63, 105, 55, 71, 47, 65, 58, 63, 105, 55, 71)
    initial_delay = random.randrange(1, 23) * 60
    time.sleep(initial_delay)
    for interval in intervals:
        scrape_once.run()
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
