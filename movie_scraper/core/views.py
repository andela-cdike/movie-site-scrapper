from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from core.exceptions import (
    InvalidPageStructureException, ServerException,
    ServiceUnavailable, SiteFetchException
)
from core.scrapper import get_movies, search_movie


URL = 'https://silverbirdcinemas.com/cinema/accra/'


class MoviesAPIView(APIView):
    """
    The base operation of all movie views is abstracted here
    """

    def get_movies(self, request):
        try:
            movies = get_movies(URL)
        except InvalidPageStructureException:
            raise ServerException(
                {'error': f'The structure of the site: {URL} has changed'})
        except SiteFetchException as exc:
            raise ServiceUnavailable(str(exc))

        return movies



class MovieSearch(MoviesAPIView):
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

        movies = self.get_movies(request)
        movies = sorted(movies, key= lambda movie: movie['title'].lower())
        movie = search_movie(movie_title, movies)
        if not movie:
            raise NotFound({'msg': 'Movie not found'})

        return Response(data=movie)


class MoviesList(MoviesAPIView):
    """List all Movies scrapped"""

    def get(self, request, *args, **kwargs):
        """
        /api/v1/movies/
        """
        return Response(self.get_movies(request))


class MovieRetrieve(MoviesAPIView):
    """Retrieve a move by its index in the list of movies"""

    def get(self, request, movie_id, *args, **kwargs):
        """
        /api/v1/movies/<movie_id>/
        """
        movies = self.get_movies(request)
        try:
            movie = movies[movie_id]
        except IndexError:
            raise NotFound()
        return Response(movie)
