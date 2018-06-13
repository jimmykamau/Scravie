from django.core.management.base import BaseCommand, CommandError

from scravie.api.scraper.utils import cache_movies


class Command(BaseCommand):
    help = 'Scraps the movies from the server and caches them'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Caching movies...'))
        message, response = cache_movies()
        if message == "success":
            self.stdout.write(self.style.SUCCESS('Successfully cached movies'))
        else:
            raise CommandError('{}'.format(response))
