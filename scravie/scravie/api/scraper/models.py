from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100)
    details_url = models.URLField()
    thumbnail_url = models.URLField()
    duration = models.CharField(max_length=50)
    days_showing = models.CharField(max_length=50)
    time_showing = models.CharField(max_length=100)


class Person(models.Model):
    name = models.CharField(max_length=100)


class MovieDetail(models.Model):
    movie = models.ForeignKey(
        Movie, related_name='movie_details', on_delete=models.CASCADE)
    banner_url = models.URLField()
    thumbnail_url = models.URLField()
    actors = models.ManyToManyField(Person, related_name='movie_actors')
    directors = models.ManyToManyField(Person, related_name='movie_directors')
    synopsis = models.TextField()
