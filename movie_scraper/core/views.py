from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from core.scrapper import get_movies, search_movie


URL = 'https://silverbirdcinemas.com/cinema/accra/'


class MovieSearch(APIView):
    """
    Exposes an endpoint to search for a specific movie by title
    """

    def get(self, request, *args, **kwargs):
        """
        /api/v1/movies/?search=movie_id
        """
        try:
            movie_title = request.query_params['movie_title']
        except KeyError:
            raise ValidationError(
                {'error': 'movie_title not supplied in query params'})

        movies = get_movies(URL)
        movies = sorted(movies, key= lambda movie: movie['title'])
        movie = search_movie(movie_title, movies)
        if not movie:
            raise NotFound({'msg': 'Movie not found'})

        return Response(data=movie)


class MoviesList(APIView):
    """List all Movies scrapped"""

    def get(self, request, *args, **kwargs):
        """
        /api/v1/movies/
        """
        movies = get_movies(URL)
        return Response(movies)


class MovieRetrieve(APIView):
    """Retrieve a move by its index in the list of movies"""

    def get(self, request, movie_id, *args, **kwargs):
        """
        /api/v1/movies/<movie_id>/
        """
        try:
            movie = get_movies(URL)[movie_id]
        except IndexError:
            raise NotFound()
        return Response(movie)
