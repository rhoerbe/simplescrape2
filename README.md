# README

## Purpose 

Scrape data from a given Website search result and detect changes. 
Send a message if a change has been found.

## Concept

### main.py
main.py will periodically execute scrape_once. 
The duration and scraping frequency can be parametrized. 
main.py should be invoked from cron, e.g. daily for robustness.

### scrape_once
Execute scrape flows, aggregates, logs and messages any results.

### scraper_willhaben

The best method to get search result items is to load the URLs from a JSON embedded in a SCRIPT tag.
(reading the page and searching for filtering links requires Selenium magic to render the full page by scrolling downwards.)


## Setup Linux

install python 3.11
on alamalinux 9/minimal `dnf install chromium`
cd /opt
git clone <repo>
create + activate venv 
pip install -r requirements.txt
cp main_default.sh main.sh + edit env vars
test main.sh: see if telegram message uis delivered upon detecting a diff
setup cron for main.sh
