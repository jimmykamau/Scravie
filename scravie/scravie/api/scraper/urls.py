from django.urls import path

from scravie.api.scraper import views

urlpatterns = [
    path('', views.ListMovieView.as_view(), name='movie-api')
]
