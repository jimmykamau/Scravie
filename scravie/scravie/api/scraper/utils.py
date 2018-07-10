import calendar
import datetime
from contextlib import closing

import pytz
import requests
import scravie.api.scraper.models as scraper_models
import scravie.api.scraper.serializers as scraper_serializers
from bs4 import BeautifulSoup


def get_airing_timestamps(days, times):
    today_datetime = datetime.datetime.today()
    days = [item if item != "Thur" and item !=
            "THUR" else "Thu" for item in days.split()]
    if '-' in days:
        days.remove('-')
    days = list(map(str.upper, days))
    days_list = list(map(str.upper, list(calendar.day_abbr)))
    today_index = days_list.index(today_datetime.strftime("%a").upper())
    start_index = days_list.index(days[0])
    end_index = days_list.index(days[1]) if (len(days) > 1) else None
    days_showing = list()
    if end_index is not None:
        if (start_index > end_index):
            days_showing = days_list[end_index:] + days_list[:start_index+1]
        else:
            days_showing = days_list[start_index:end_index+1]
    else:
        days_showing.append(days_list[start_index])
    timestamps = list()
    for day in days_showing:
        day_index = days_list.index(day)
        day_difference = 0
        if (day_index > today_index):
            day_difference = day_index - today_index
        else:
            day_difference = (7 - today_index) + day_index
        for time in list(map(str.strip, times.split(","))):
            show_time = datetime.datetime.strptime(time, "%I:%M%p")
            timestamp_showing = (today_datetime + datetime.timedelta(days=day_difference)).replace(
                hour=show_time.hour, minute=show_time.minute,
                second=0, microsecond=0, tzinfo=pytz.UTC)
            timestamps.append(dict(time_showing=timestamp_showing.isoformat()))
    return timestamps


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
    movie_info['times_showing'] = get_airing_timestamps(
        movie_info['days_showing'], movie_info['time_showing'])
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
    movie_models = scraper_models.Movie.objects.all()
    if movie_models.exists():
        movie_models.delete()
        scraper_models.Person.objects.all().delete()
        scraper_models.TimesShowing.objects.all().delete()
    movie_serializer = scraper_serializers.MovieSerializer(
        data=movies, many=True)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return "success", movie_serializer.data
    else:
        return "error", movie_serializer.errors
