from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('hospital.HomePage')

    # Delete the default homepage
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='hospital')

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Hospital Homepage",
        draft_title="Hospital Homepage",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost',
        root_page=homepage,
        is_default_site=True
    )


def create_blog_index(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    BlogIndexPage = apps.get_model('hospital.BlogIndexPage')
    HomePage = apps.get_model('hospital.HomePage')

    # Get homepage
    homepage = HomePage.objects.get(slug='home')

    # Create content type for blog index page
    blog_index_content_type, created = ContentType.objects.get_or_create(
        model='blogindexpage', app_label='hospital')

    # Create blog index page
    blogindex = BlogIndexPage.objects.create(
        title="Blog",
        draft_title="Blog",
        slug='blog',
        content_type=blog_index_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/home/blog/',
        intro="Welcome to our hospital blog!"
    )

    # Add blog index page as child of homepage
    homepage.numchild += 1
    homepage.save()


def create_doctor_index(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    DoctorIndexPage = apps.get_model('hospital.DoctorIndexPage')
    HomePage = apps.get_model('hospital.HomePage')

    # Get homepage
    homepage = HomePage.objects.get(slug='home')

    # Create content type for doctor index page
    doctor_index_content_type, created = ContentType.objects.get_or_create(
        model='doctorindexpage', app_label='hospital')

    # Create doctor index page
    doctorindex = DoctorIndexPage.objects.create(
        title="Doctors",
        draft_title="Doctors",
        slug='doctors',
        content_type=doctor_index_content_type,
        path='000100010002',
        depth=3,
        numchild=0,
        url_path='/home/doctors/',
        intro="Meet our professional doctors."
    )

    # Update homepage child count
    homepage.numchild += 1
    homepage.save()


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.RunPython(create_homepage),
        migrations.RunPython(create_blog_index),
        migrations.RunPython(create_doctor_index),
    ]