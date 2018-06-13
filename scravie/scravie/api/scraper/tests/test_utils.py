from rest_framework.test import APITestCase

import scravie.api.scraper.utils as scraper_utils
import scravie.api.scraper.models as scraper_models


class ScraperUtilsTestCase(APITestCase):

    def setUp(self):
        self.html_data = scraper_utils.get_html_data(
            "https://silverbirdcinemas.com/cinema/accra/"
        )

    def test_get_html_data(self):
        self.assertIsNotNone(self.html_data)

    def test_scrap_data(self):
        data = scraper_utils.scrap_data()[0]
        self.assertCountEqual(
            ['name', 'details_url', 'thumbnail_url', 'duration',
                'days_showing', 'time_showing', 'movie_details'],
            data
        )

    def test_cache_movies(self):
        scraper_utils.cache_movies()
        self.assertIsNotNone(
            scraper_models.Movie.objects.first()
        )
