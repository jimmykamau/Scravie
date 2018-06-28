from django.urls import path

from scravie.api.scraper import views

urlpatterns = [
    path('', views.ListMovieView.as_view(), name='movie-api'),
    path('search/', views.ListMovieSearchView.as_view(), name='search-api-view'),
    path('<slug:id>/', views.ListMovieDetailView.as_view(), name='movie-detail-api')
]
