from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.serializers as scraper_serializers


class ListMovieView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = scraper_models.Movie.objects.all()
    serializer_class = scraper_serializers.MovieSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'name')


class ListMovieDetailView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = scraper_serializers.MovieDetailSerializer

    def get_queryset(self):
        movie_id = self.kwargs['id']
        return scraper_models.MovieDetail.objects.filter(movie__id=movie_id)
