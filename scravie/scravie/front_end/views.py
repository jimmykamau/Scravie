import requests
import scravie.front_end.forms as front_end_forms
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get(self, request):
        search_form = front_end_forms.SearchForm()
        movies_api_url = request.build_absolute_uri(reverse('movie-api'))
        movies_data = requests.get(
            movies_api_url,
            headers={"Content-Type": "application/json"}
        )
        context = dict(movies=movies_data.json(), search_form=search_form)
        return render(request, 'index.html', context)

    def post(self, request):
        search_form = front_end_forms.SearchForm(request.POST)
        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            search_api_url = '{}?name={}'.format(
                request.build_absolute_uri(reverse('search-api-view')), search_query)
            movies_data = requests.get(
                search_api_url,
                headers={"Content-Type": "application/json"}
            )
            context = dict(
                movies=movies_data.json(), search_string=search_query, search_form=search_form)
            return render(request, 'index.html', context)


class DetailView(TemplateView):
    def get(self, request, id):
        movie_detail_api_url = '{}?id={}'.format(
            request.build_absolute_uri(reverse('movie-api')),
            id)
        movie_detail_data = requests.get(
            movie_detail_api_url,
            headers={"Content-Type": "application/json"}
        )
        context = dict(movie=movie_detail_data.json()[0])
        return render(request, 'detail.html', context)


class SortNameView(TemplateView):
    def get(self, request):
        sort_api_url = '{}?sort_by=name'.format(
            request.build_absolute_uri(reverse('sort-api-view')))
        movies_data = requests.get(
            sort_api_url,
            headers={"Content-Type": "application/json"}
        )
        context = dict(movies=movies_data.json())
        return render(request, 'index.html', context)


class SearchDateView(TemplateView):
    def post(self, request):
        date_search_form = front_end_forms.DateSearchForm(request.POST)
        if date_search_form.is_valid():
            date_query = date_search_form.cleaned_data['date_query']
            search_api_url = request.build_absolute_uri(
                reverse('sort-date-api-view', kwargs={'date': date_query}))
            timings_data = requests.get(
                search_api_url,
                headers={"Content-Type": "application/json"}
            )
            context = dict(timings=timings_data.json(), show_date=date_query)
            return render(request, 'search_date.html', context)
