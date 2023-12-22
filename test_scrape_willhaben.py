import pytest
import re
from scrape_willhaben import ScrapeWillhaben

@pytest.mark.selenium
def test_scrape_method():
    scraping_target_host = "https://www.willhaben.at"
    scraping_target_path = "/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=b593acc8-1647-4ba6-adfc-1d0e51802baa&isNavigation=true&areaId=900&NO_OF_ROOMS_BUCKET=3X3&NO_OF_ROOMS_BUCKET=4X4&PROPERTY_TYPE=113&ESTATE_SIZE/LIVING_AREA_FROM=60"
    filter_detail_link = re.compile(r'/iad/immobilien/d/mietwohnungen/wien')

    scraper = ScrapeWillhaben()
    result = scraper.scrape(scraping_target_host, scraping_target_path, filter_detail_link)
    print('\n'.join(result))

    # Add assertions based on the expected behavior of the scrape method
    # For example, you might assert on the number of items returned
    assert len(result) > 0  # true only if search result > 0 -> usually the case ;-)
    # Add more assertions as needed

# Note: The @pytest.mark.selenium decorator is added to this test function
# This allows you to selectively run tests with the 'selenium' marker
# You can run only the selenium tests using: pytest -m selenium
