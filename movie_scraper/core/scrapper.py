from bs4 import BeautifulSoup
import requests

from core.exceptions import InvalidPageStructureException, SiteFetchException 


def get_movies(url):
    """
    Returns movie information from the supplied URL
    :param url: string
    :return: list of dicts
    """
    try:
        resp = requests.get(url)
    except (ConnectionError, requests.exceptions.RequestException) as exc:
        raise SiteFetchException(str(exc))
    soup = BeautifulSoup(resp.content, 'html.parser')
    try:
        return extract_movie_details(soup)
    except (AttributeError, IndexError):
        raise InvalidPageStructureException


def extract_movie_details(soup):
    """
    Extract information about movies from the Beautiful Soup object
    by using beautiful soup traversal utilities
    :param soup: BeautifulSoup
    :return: a list of dicts
    """
    grid_items = soup.find_all(class_='amy-ajax-content')[0]
    movies = []
    for grid_item in grid_items:
        movie = {}
        movie['title'] = grid_item.find('h4').a.string

        entry_content = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0]

        movie['date'] = entry_content.find_all(class_='entry-date')[0].getText()
        movie['date_showing'] = entry_content.find_all(class_='cinema_page_showtime')[0].getText().replace('Showtime: ', '')

        desc_mv = entry_content.find_all(class_='desc-mv')[0]
        movie['genre'] = desc_mv.div.getText().replace('Release:', '')
        movie['language'] = desc_mv.find_all(class_='note')[0].getText().replace('Genre:', '')
        movie['release'] = desc_mv.find_all('div')[2].getText().replace('Language:', '')

        movie['rating'] = entry_content.find_all(class_='entry-rating')[0].find_all(class_='rate')[0].getText()

        movies.append(movie)

    return movies



def search_movie(movie_title, movies):
    """
    Search for a movie_title among the list of movies supplied
    :param movie_title: string
    :param movies: list of dicts
    :return: a movie dictionary object or None
    """
    if len(movies) < 1:
        return None

    mid = len(movies) // 2
    if movie_title.lower() == movies[mid]['title'].lower():
        return movies[mid]
    elif movie_title.lower() < movies[mid]['title'].lower():
        return search_movie(movie_title, movies[:mid])
    elif movie_title.lower() > movies[mid]['title'].lower():
        return search_movie(movie_title, movies[mid + 1:])
