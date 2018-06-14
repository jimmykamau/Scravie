from contextlib import closing
import sqlite3

import requests

import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.serializers as scraper_serializers
from bs4 import BeautifulSoup


def get_html_data(url):
    try:
        with closing(requests.get(url, stream=True)) as response:
            return response.content
    except requests.RequestException as e:
        print("{}".format(e))


def get_movies_data(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    return soup.find_all("article", class_="entry-item")


def get_movie_details_data(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    return soup.find("div", id="content")


def get_movie_info(movie_data):
    movie_info = dict()
    movie_title_data = movie_data.find(
        "h4", class_="entry-title").contents[0]
    movie_info['name'] = movie_title_data.string
    movie_info['details_url'] = movie_title_data.get('href')
    movie_info['thumbnail_url'] = movie_data.find(
        "img").get('src')
    movie_info['duration'] = movie_data.find(
        "div", class_="entry-date").contents[1]
    movie_show_dates_data = movie_data.find(
        "p", class_="cinema_page_showtime").contents
    movie_info['days_showing'] = movie_show_dates_data[2].string.split(":")[
        0].strip()
    movie_info['time_showing'] = movie_show_dates_data[3].string.strip()
    return movie_info


def get_movie_details(movie_info):
    details_url = movie_info['details_url']
    html_data = get_html_data(details_url)
    if html_data is not None:
        movie_details_data = get_movie_details_data(html_data)
        movie_details = dict()
        movie_details['banner_url'] = movie_details_data.find(
            "section", id="amy-page-header").contents[1].get('src')
        movie_details['thumbnail_url'] = movie_details_data.find(
            "div", class_="entry-thumb").contents[1].get('src')
        movie_details_info_list = movie_details_data.find(
            "ul", class_="info-list").find_all("li")
        movie_details['actors'] = [
            {"name": actor.text} for actor in movie_details_info_list[0].find_all("a")]
        movie_details['directors'] = [
            {"name": director.text} for director in movie_details_info_list[1].find_all("a")]
        movie_details['synopsis'] = movie_details_data.find(
            "div", class_=["entry-content", "e-content"]).contents[3].string
        return movie_details


def scrap_data():
    movies_url = "https://silverbirdcinemas.com/cinema/accra/"
    html_data = get_html_data(movies_url)
    if html_data is not None:
        movies_data = get_movies_data(html_data)
        movies_info_list = []
        for movie_data in movies_data:
            movie_info = get_movie_info(movie_data)
            movie_details = get_movie_details(movie_info)
            movie_info['movie_details'] = [movie_details]
            movies_info_list.append(movie_info)
        return movies_info_list


def cache_movies():
    movies = scrap_data()
    try:
        scraper_models.Movie.objects.all().delete()
        scraper_models.Person.objects.all().delete()
    except sqlite3.OperationalError:
        # Mostly happens on first app run
        pass

    movie_serializer = scraper_serializers.MovieSerializer(data=movies, many=True)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return "success", movie_serializer.data
    else:
        return "error", movie_serializer.errors
