from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Page, Site
from hospital.models import HomePage

class Command(BaseCommand):
    help = 'Setup initial Wagtail data'

    def handle(self, *args, **options):
        # Delete the default homepage if it exists
        Page.objects.filter(slug='home').delete()

        # Get the root page
        root_page = Page.objects.get(id=1)

        # Create a new homepage
        homepage = HomePage(
            title="Hospital Homepage",
            slug='home',
            content_type=ContentType.objects.get_for_model(HomePage),
            show_in_menus=True,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )

        root_page.add_child(instance=homepage)

        # Create a default site
        Site.objects.all().delete()
        Site.objects.create(
            hostname='localhost',
            root_page=homepage,
            is_default_site=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up initial data')) 