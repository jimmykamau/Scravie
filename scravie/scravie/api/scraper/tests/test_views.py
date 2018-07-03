import datetime

import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.utils as scraper_utils
from django.urls import reverse
from rest_framework.test import APITestCase


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
            ['id', 'name', 'details_url', 'thumbnail_url',
             'duration', 'days_showing', 'time_showing',
             'movie_details', 'times_showing'],
            response.data[0]
        )


class ListMovieDetailViewTest(APITestCase):
    def setUp(self):
        self.movies_status, self.movies_response = scraper_utils.cache_movies()
        self.movie = scraper_models.Movie.objects.first()
        self.url = reverse('movie-detail-api', kwargs={'id': self.movie.id})

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(
            200, response.status_code
        )
        self.assertCountEqual(
            ['banner_url', 'thumbnail_url', 'actors', 'directors', 'synopsis'],
            response.data[0]
        )


class ListMovieSearchViewTest(APITestCase):
    def setUp(self):
        scraper_utils.cache_movies()
        self.movie_name = scraper_models.Movie.objects.first().name
        self.url = '{}?name={}'.format(
            reverse('search-api-view'), self.movie_name)

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(
            200, response.status_code
        )
        self.assertEqual(
            self.movie_name, response.data[0]['name']
        )


class ListMovieSortViewTest(APITestCase):
    def setUp(self):
        scraper_utils.cache_movies()
        self.url = '{}?sort_by=name'.format(reverse('sort-api-view'))

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        movie_names = [movie['name'] for movie in response.data]
        self.assertEqual(
            sorted(movie_names), movie_names
        )


class ListMovieSortDatetimeViewTest(APITestCase):
    def setUp(self):
        scraper_utils.cache_movies()
        tomorrow_datetime = datetime.date.today() + datetime.timedelta(days=1)
        self.url = reverse(
            'sort-date-api-view', kwargs={'date': datetime.datetime.strftime(
                tomorrow_datetime, "%Y-%m-%d")
            }
        )

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        times_list = response.data['data'].keys()
        timestamp_list = [datetime.datetime.strptime(
            timestamp, "%I:%M%p") for timestamp in times_list]
        self.assertEqual(
            sorted(timestamp_list), timestamp_list
        )
