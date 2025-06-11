from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Page, Site
from hospital.models import HomePage, ServiceIndexPage, BlogIndexPage, DoctorIndexPage

class Command(BaseCommand):
    help = 'Initialize Wagtail site structure'

    def handle(self, *args, **options):
        # Get the root page
        root_page = Page.objects.first()
        
        if root_page:
            # Create HomePage
            home_page = HomePage(
                title="Hospital Management System",
                slug='home',
                body='Welcome to our Hospital Management System'
            )
            root_page.add_child(instance=home_page)
            
            # Create ServiceIndexPage
            services_page = ServiceIndexPage(
                title="Our Services",
                slug='services',
                intro='Explore our wide range of medical services'
            )
            home_page.add_child(instance=services_page)
            
            # Create BlogIndexPage
            blog_page = BlogIndexPage(
                title="Blog",
                slug='blog',
                intro='Stay updated with our latest medical insights'
            )
            home_page.add_child(instance=blog_page)
            
            # Create DoctorIndexPage
            doctors_page = DoctorIndexPage(
                title="Our Doctors",
                slug='doctors',
                intro='Meet our experienced medical professionals'
            )
            home_page.add_child(instance=doctors_page)
            
            # Set up the default site
            hostname = 'localhost'
            port = 80
            
            # Delete any existing sites
            Site.objects.all().delete()
            
            # Create a new site with the home page as root
            Site.objects.create(
                hostname=hostname,
                port=port,
                root_page=home_page,
                is_default_site=True
            )
            
            self.stdout.write(self.style.SUCCESS("Wagtail site structure created successfully!"))
        else:
            self.stdout.write(self.style.ERROR("No root page found. Please ensure Wagtail is properly installed.")) 