import requests
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get(self, request):
        movies_api_url = request.build_absolute_uri(reverse('movie-api'))
        movies_data = requests.get(
            movies_api_url,
            headers={"Content-Type": "application/json"}
        )
        context = dict(movies=movies_data.json())
        return render(request, 'index.html', context)
