from rest_framework.test import APITestCase

import scravie.api.scraper.utils as scraper_utils


class ScraperUtilsTestCase(APITestCase):
    
    def setUp(self):
        self.html_data = scraper_utils.get_html_data(
            "https://silverbirdcinemas.com/cinema/accra/"
        )

    def test_get_html_data(self):
        self.assertIsNotNone(self.html_data)

    def test_scrap_data(self):
        self.assertCountEqual(
            ['name', 'details_url', 'thumbnail', 'duration', 'days_showing', 'time_showing', 'details'],
            scraper_utils.scrap_data()[0]
        )
