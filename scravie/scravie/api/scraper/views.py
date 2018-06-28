import functools
import operator

import django.contrib.postgres.search as postgres_search
import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.serializers as scraper_serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions


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


class ListMovieSearchView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = scraper_serializers.MovieSerializer

    def get_queryset(self):
        queryset = scraper_models.Movie.objects.all()
        search_string = self.request.query_params.get('name', None)
        if search_string is not None:
            terms = [postgres_search.SearchQuery(
                term) for term in search_string.split()]
            vector = postgres_search.SearchVector('name')
            query = functools.reduce(operator.or_, terms)
            queryset = scraper_models.Movie.objects.annotate(
                rank=postgres_search.SearchRank(vector, query)
            ).order_by('-rank').filter(rank__gte=0.06)
        return queryset


class ListMovieSortView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = scraper_serializers.MovieSerializer

    def get_queryset(self):
        queryset = scraper_models.Movie.objects.all()
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by is not None:
            queryset = queryset.order_by(sort_by)
        return queryset
