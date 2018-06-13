from rest_framework import generics, permissions

import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.serializers as scraper_serializers


class ListMovieView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = scraper_models.Movie.objects.all()
    serializer_class = scraper_serializers.MovieSerializer
