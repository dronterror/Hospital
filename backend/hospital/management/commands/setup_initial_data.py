from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from hospital.models import HomePage, DoctorIndexPage
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Sets up initial data for the hospital website'

    @transaction.atomic
    def handle(self, *args, **options):
        if HomePage.objects.exists():
            self.stdout.write('Homepage already exists')
            return

        try:
            # Get root page
            root = Page.objects.get(id=1)

            # Delete any existing child pages of root
            root.get_children().delete()

            # Create homepage
            homepage_content_type = ContentType.objects.get_for_model(HomePage)
            homepage = HomePage(
                title="Hospital Home",
                draft_title="Hospital Home",
                slug='home',
                intro="Welcome to our Hospital Management System",
                show_in_menus=True,
                content_type=homepage_content_type,
                path='00010001',
                depth=2,
                numchild=0,
                url_path='/home/',
            )

            root.add_child(instance=homepage)

            # Create or update the default site
            Site.objects.update_or_create(
                hostname='localhost',
                defaults={
                    'root_page': homepage,
                    'is_default_site': True,
                    'site_name': 'Hospital Website'
                }
            )

            # Create doctor index page
            doctor_index_content_type = ContentType.objects.get_for_model(DoctorIndexPage)
            doctor_index = DoctorIndexPage(
                title="Our Doctors",
                draft_title="Our Doctors",
                slug='doctors',
                intro="Meet our experienced medical professionals",
                show_in_menus=True,
                content_type=doctor_index_content_type,
                path='000100010001',
                depth=3,
                numchild=0,
                url_path='/home/doctors/',
            )

            homepage.add_child(instance=doctor_index)

            self.stdout.write(self.style.SUCCESS('Successfully set up initial data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error setting up initial data: {str(e)}')) 