from django.urls import path

import scravie.front_end.views as front_end_views

urlpatterns = [
    path('', front_end_views.IndexView.as_view(), name='movies')
]
