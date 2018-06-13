from django.urls import path

from scravie.api.scraper import views

urlpatterns = [
    path('', views.ListMovieView.as_view(), name='movie-api'),
    path('<slug:id>/', views.ListMovieDetailView.as_view(), name='movie-detail-api')
]
