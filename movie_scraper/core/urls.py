from django.urls import include, path

from core import views


urlpatterns = [
    path('movies/', views.MoviesList.as_view(), name='movies-list'),
    path('search_movie/', views.MovieSearch.as_view(), name='movie-search'),
    path('movies/<int:movie_id>/',
         views.MovieRetrieve.as_view(), name='movie-retrieve'),
]
