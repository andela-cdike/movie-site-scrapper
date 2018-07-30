import uuid
from unittest import TestCase
from unittest.mock import patch

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from core.exceptions import InvalidPageStructureException, SiteFetchException
from core.scrapper import extract_movie_details, get_movies, search_movie


EXPECTED_MOVIES = [
    "MISSION IMPOSSIBLE: FALLOUT",
    "SKYSCRAPER",
    "Ant-Man and the Wasp",
    "OCEAN'S 8",
    "Mamma Mia! Here We Go Again",
    "HOTEL TRANSYLVANIA 3: A SUMMER VACATION",
    "Incredibles 2"
]


def get_movies_for_test():
    movies = []
    for movie in EXPECTED_MOVIES:
        movies.append({'title': movie, 'random_field': uuid.uuid4()})

    return movies


class MockMovieSiteResponse:

    def __init__(self, *args, **kwargs):
        with open(f'{settings.BASE_DIR}/core/tests/sample_html_response.html') as fp:
            self.content = fp.read()


class GetMoviesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'http://fake-site.com'

    @patch('core.scrapper.requests.get',
           side_effect=requests.exceptions.ConnectionError)
    def test_when_site_fetch_fails(self, _):
        self.assertRaises(SiteFetchException, get_movies, self.url)

    @patch('core.scrapper.requests.get', return_value=MockMovieSiteResponse())
    @patch('core.scrapper.extract_movie_details')
    def test_calls_extract_movie_detailss_with_soup_object(self, mock_extract_movie_details, _):
        response = get_movies(self.url)
        mock_extract_movie_details.called_once()
        mock_extract_movie_details.call_args[0][0] == BeautifulSoup

    @patch('core.scrapper.requests.get', return_value=MockMovieSiteResponse())
    @patch('core.scrapper.extract_movie_details', side_effect=AttributeError)
    def test_raises_exception_when_page_structure_changes(
            self, mock_extract_movie_details, mock_get_requests):
        self.assertRaises(InvalidPageStructureException, get_movies, self.url)

    @patch('core.scrapper.requests.get', return_value=MockMovieSiteResponse())
    def test_get_movies_successful(self, mock_get_request):
        derived_movies = get_movies(self.url)
        for derived_movie, expected_movie in zip(
                sorted(derived_movies, key= lambda movie: movie['title']),
                sorted(EXPECTED_MOVIES)):
            self.assertEqual(derived_movie['title'], expected_movie)



class ExtractMovieDetailTest(TestCase):

    def test_extract_movie_details_successful(self):
        with open(f'{settings.BASE_DIR}/core/tests/sample_html_response.html') as fp:
            content = fp.read()
        soup = BeautifulSoup(content, 'html.parser')
        derived_movies = extract_movie_details(soup)

        for derived_movie, expected_movie in zip(
                sorted(derived_movies, key= lambda movie: movie['title']),
                sorted(EXPECTED_MOVIES)):
            self.assertEqual(derived_movie['title'], expected_movie)


class SearchMovieTest(TestCase):
    @classmethod
    def setUpClass(cls):
        movies = get_movies_for_test()
        cls.movies = sorted(movies, key= lambda movie: movie['title'].lower())

    def test_search_movie_finds_all_movies(self):
        for movie in EXPECTED_MOVIES:
            self.assertEqual(search_movie(movie, self.movies)['title'], movie)

    def test_search_movie_not_in_list(self):
        self.assertIsNone(search_movie('Invalid', self.movies))
