from bs4 import BeautifulSoup
import requests


def fetch_site(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def get_movies(url):
    soup = fetch_site(url)
    grid_items = soup.find_all(class_='amy-ajax-content')[0]
    movies = []
    for grid_item in grid_items:
        movie = {}
        movie['title'] = grid_item.find('h4').a.string
        movie['date'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='entry-date')[0].getText()
        movie['date_showing'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='cinema_page_showtime')[0].getText().replace('Showtime: ', '')
        movie['genre'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].div.getText().replace('Release:', '')
        movie['language'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].find_all(class_='note')[0].getText().replace('Genre:', '')
        movie['release'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].find_all('div')[2].getText().replace('Language:', '')
        movie['rating'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='entry-rating')[0].find_all(class_='rate')[0].getText()

        movies.append(movie)

    return movies



def search_movie(movie_title, movies):
    """
    expects sorted movies by title
    """
    if len(movies) < 1:
        return None

    mid = len(movies) // 2
    if movie_title == movies[mid]['title']:
        return movies[mid]
    elif movie_title < movies[mid]['title']:
        return search_movie(movie_title, movies[:mid])
    elif movie_title > movies[mid]['title']:
        return search_movie(movie_title, movies[mid + 1:])


# {
#     'title': '',
#     'date': '',
#     'date showing': '',
#     'genre': '',
#     'language': '',
#     'release': '',
#     'rating': '',
# }
# movies = []
# for grid_item in grid_items:
#     movie = {}
#     movie['title'] = grid_item.find('h4').a.string
#     movie['date'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='entry-date')[0].getText()
#     movie['date_showing'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='cinema_page_showtime')[0].getText().replace('Showtime: ', '')
#     movie['genre'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].div.getText().replace('Release:', '')
#     movie['language'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].find_all(class_='note')[0].getText().replace('Genre:', '')
#     movie['release'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='desc-mv')[0].find_all('div')[2].getText().replace('Language:', '')
#     movie['rating'] = grid_item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='entry-rating')[0].find_all(class_='rate')[0].getText()


# for item in grid_items.find_all(class_='grid-item'):
#     print(item.find_all(class_='entry-item')[0].find_all(class_='entry-content')[0].find_all(class_='entry-date'))