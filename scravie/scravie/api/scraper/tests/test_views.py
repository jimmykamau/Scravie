from django.urls import reverse
from rest_framework.test import APITestCase

import scravie.api.scraper.utils as scraper_utils


class ListMovieViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('movie-api')
        scraper_utils.cache_movies()

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(
            200, response.status_code
        )
        self.assertCountEqual(
            ['name', 'details_url', 'thumbnail_url', 'duration',
                'days_showing', 'time_showing', 'movie_details'],
            response.data[0]
        )
