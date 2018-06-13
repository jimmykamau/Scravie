from rest_framework import serializers

import scravie.api.scraper.models as scraper_models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = scraper_models.Person
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    actors = PersonSerializer(many=True)
    directors = PersonSerializer(many=True)

    class Meta:
        model = scraper_models.MovieDetail
        fields = ('banner_url', 'thumbnail_url',
                  'actors', 'directors', 'synopsis')


class MovieSerializer(serializers.ModelSerializer):
    movie_details = MovieDetailSerializer(many=True)

    class Meta:
        model = scraper_models.Movie
        fields = ('name', 'details_url', 'thumbnail_url',
                  'duration', 'days_showing', 'time_showing', 'movie_details')

    def create(self, validated_data):
        movie_details_data = validated_data.pop('movie_details')
        movie = scraper_models.Movie.objects.create(**validated_data)
        for detail in movie_details_data:
            actors = detail.pop('actors')
            directors = detail.pop('directors')
            instance = scraper_models.MovieDetail.objects.create(movie=movie, **detail)
            actors_model_list = []
            for actor in actors:
                actor_model, created = scraper_models.Person.objects.get_or_create(
                    **actor)
                actors_model_list.append(actor_model)
            directors_model_list = []
            for director in directors:
                director_model, created = scraper_models.Person.objects.get_or_create(
                    **director)
                directors_model_list.append(director_model)
            instance.actors.set(actors_model_list)
            instance.directors.set(directors_model_list)
        return movie
