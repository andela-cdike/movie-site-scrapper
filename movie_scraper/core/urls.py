from django.urls import include, path

from core import views


urlpatterns = [
    path('search_movie/', views.SearchMovie.as_view(), name='search-movie'),
    path('get_movies/', views.GetMovies.as_view(), name='get-movies')
]
