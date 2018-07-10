from django.contrib import admin

import scravie.api.scraper.models as scraper_models

admin.site.register(scraper_models.Movie)
admin.site.register(scraper_models.MovieDetail)
admin.site.register(scraper_models.Person)
