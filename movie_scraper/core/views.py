from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from core.scrapper import get_movies, search_movie


URL = 'https://silverbirdcinemas.com/cinema/accra/'


class SearchMovie(APIView):
    def get(self, request, *args, **kwargs):
        try:
            movie_title = request.query_params['movie_title']
        except KeyError:
            raise ValidationError({'error': 'movie_title not supplied in query params'})

        movies = get_movies(URL)
        movies = sorted(key= lambda movie: movie['title'])
        movie = search_movie(movie_title, movies)
        if not movie:
            return Response(200, data={'msg': 'movie not found'})

        return Response(200, data=movie)


class GetMovies(APIView):
    def get(self, request, *args, **kwargs):
        movies = get_movies(URL)
        return Response(200, data=movies)
