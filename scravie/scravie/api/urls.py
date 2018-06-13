from django.urls import include, path

urlpatterns = [
    path('movie/', include('scravie.api.scraper.urls'))
]
