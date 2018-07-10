from django.urls import path

import scravie.front_end.views as front_end_views

urlpatterns = [
    path('', front_end_views.IndexView.as_view(), name='movies'),
    path('date-filter/', front_end_views.SearchDateView.as_view(), name='date-filter'),
    path('sort-by-name/', front_end_views.SortNameView.as_view(), name='sort-by-name'),
    path('movie-detail/<slug:id>/', front_end_views.DetailView.as_view(), name='movie-detail')
]
