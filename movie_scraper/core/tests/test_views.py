from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


MOVIE_LIST = [
    {'title': 'The Bread my sweet'},
    {'title': 'Ravenclaw'}
]


@patch('core.views.get_movies', return_value=MOVIE_LIST)
class MovieSearchTest(TestCase):
    def test_search_movie_without_providing_search_term(self, _):
        response = self.client.get(reverse('movie-search'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'error': 'movie_title not supplied in query params'})

    def test_search_movie_not_exist(self, _):
        response = self.client.get(
            reverse('movie-search') + '?movie_title=Invalid')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'msg': 'Movie not found'})

    def test_search_movie_exist(self, movies_mock):
        response = self.client.get(
            reverse('movie-search') + '?movie_title=Ravenclaw')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Ravenclaw'})


class MovieListTest(TestCase):
    @patch('core.views.get_movies', return_value=MOVIE_LIST)
    def test_list_movie(self, movies_mock):
        response = self.client.get(reverse('movies-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MOVIE_LIST)

    @patch('core.views.get_movies', return_value=[])
    def test_list_empty_movie(self, movies_mock):
        response = self.client.get(reverse('movies-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

@patch('core.views.get_movies', return_value=MOVIE_LIST)
class MovieRetrieveTest(TestCase):
    def test_retrieve_movie_success(self, movies_mock):
        response = self.client.get(reverse('movie-retrieve',
                                   kwargs={'movie_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MOVIE_LIST[1])

    def test_retrieve_movie_failure(self, movies_mock):
        response = self.client.get(reverse('movie-retrieve',
                                   kwargs={'movie_id': 4}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
