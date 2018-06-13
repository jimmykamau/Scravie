from rest_framework import serializers

import scravie.api.scraper.models as scraper_models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = scraper_models.Person
        fields = ('name')


class MovieDetailSerializer(serializers.ModelSerializer):
    actors = PersonSerializer(many=True)
    directors = PersonSerializer(many=True)

    class Meta:
        model = scraper_models.MovieDetail
        fields = ('banner_url', 'thumbnail_url',
                  'actors', 'directors', 'synopsis')


class MovieSerializer(serializers.ModelSerializer):
    movie_details = MovieDetailSerializer()

    class Meta:
        model = scraper_models.Movie
        fields = ('name', 'details_url', 'thumbnail_url',
                  'duration', 'days_showing', 'time_showing')
