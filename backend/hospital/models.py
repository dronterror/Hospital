from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.utils import timezone
from datetime import datetime, timedelta
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.blocks import (
    CharBlock, 
    URLBlock, 
    StructBlock, 
    RichTextBlock, 
    TextBlock, 
    RawHTMLBlock,
    ChoiceBlock
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from wagtail.search import index
from wagtail.models import Orderable
from django import forms


# Original models
@register_snippet
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    doctors = models.ManyToManyField('Doctor', related_name='services')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('doctors', widget=forms.CheckboxSelectMultiple),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@register_snippet
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('user'),
        FieldPanel('date_of_birth'),
        FieldPanel('phone_number'),
        FieldPanel('address'),
        FieldPanel('medical_history'),
    ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"


@register_snippet
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    office_address = models.TextField()
    bio = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('user'),
        FieldPanel('specialization'),
        FieldPanel('license_number'),
        FieldPanel('phone_number'),
        FieldPanel('office_address'),
        FieldPanel('bio'),
    ]

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


@register_snippet
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('patient'),
        FieldPanel('doctor'),
        FieldPanel('date_time'),
        FieldPanel('reason'),
        FieldPanel('status'),
        FieldPanel('notes'),
    ]

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date_time}"


@register_snippet
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('patient'),
        FieldPanel('doctor'),
        FieldPanel('date'),
        FieldPanel('diagnosis'),
        FieldPanel('prescription'),
        FieldPanel('notes'),
    ]

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} - {self.date} - {self.diagnosis[:50]}"


@register_snippet
class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    panels = [
        FieldPanel('doctor'),
        FieldPanel('date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('is_available'),
    ]

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.date} ({self.start_time}-{self.end_time})"


# Wagtail CMS models
class CustomHTMLBlock(StructBlock):
    html_code = RawHTMLBlock(label='HTML Code')
    css_classes = CharBlock(required=False, label='CSS Classes')
    
    class Meta:
        template = 'blocks/custom_html_block.html'
        icon = 'code'
        label = 'Raw HTML'


class ContentStreamBlock(StructBlock):
    title = CharBlock(required=False, label='Title')
    content = RichTextBlock(required=False, label='Rich Text Content')
    html = RawHTMLBlock(required=False, label='HTML Code')
    
    class Meta:
        template = 'blocks/content_block.html'
        icon = 'doc-full'
        label = 'Content Block'


class HomePage(Page):
    body = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
        ('content_block', ContentStreamBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = ['hospital.ServiceIndexPage', 'hospital.BlogIndexPage', 
                    'hospital.DoctorIndexPage', 'hospital.DepartmentPage',
                    'hospital.ContactPage', 'hospital.HospitalLocationPage']
    
    class Meta:
        verbose_name = "Home Page"


class DepartmentPage(Page):
    description = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    parent_page_types = ['hospital.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['hospital.ServicePage']
    parent_page_types = ['hospital.HomePage']

    class Meta:
        verbose_name = "Services List"


class ServicePage(Page):
    description = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
        ('content_block', ContentStreamBlock()),
    ], use_json_field=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('image'),
    ]

    parent_page_types = ['hospital.ServiceIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['hospital.BlogPage']  # Only allow BlogPage as children
    
    def get_context(self, request):
        context = super().get_context(request)
        context['blog_entries'] = BlogPage.objects.child_of(self).live().order_by('-first_published_at')
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
        ('content_block', ContentStreamBlock()),
        ('custom_html', CustomHTMLBlock()),
    ], use_json_field=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]

    parent_page_types = ['hospital.BlogIndexPage']  # Can only be created under BlogIndexPage
    subpage_types = []  # This page type has no subpages

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class DoctorIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['hospital.DoctorPage']
    parent_page_types = ['hospital.HomePage']

    class Meta:
        verbose_name = "Doctors List"

    def get_context(self, request):
        context = super().get_context(request)
        context['doctors'] = DoctorPage.objects.child_of(self).live()
        return context


class NewsPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]


class ContactPage(Page):
    body = RichTextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    google_maps_link = models.URLField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('google_maps_link'),
    ]

    parent_page_types = ['hospital.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "Contact Page"


@register_snippet
class FooterSettings(models.Model):
    quick_links = StreamField([
        ('quick_link', StructBlock([
            ('link_text', CharBlock(max_length=255)),
            ('link_url', URLBlock()),
        ])),
    ], use_json_field=True)
    contact_info = RichTextField()
    social_media = StreamField([
        ('social_link', StructBlock([
            ('platform', CharBlock(max_length=50)),
            ('url', URLBlock()),
            ('icon', CharBlock(max_length=50)),
        ])),
    ], use_json_field=True)

    panels = [
        FieldPanel('quick_links'),
        FieldPanel('contact_info'),
        FieldPanel('social_media'),
    ]

    def __str__(self):
        return "Footer Settings"

    class Meta:
        verbose_name = 'Footer Settings'
        verbose_name_plural = 'Footer Settings'


@register_snippet
class EmergencyBanner(models.Model):
    message = models.TextField()
    is_active = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    
    panels = [
        FieldPanel('message'),
        FieldPanel('is_active'),
        FieldPanel('link'),
    ]


class DoctorPage(Page):
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField()
    gmc_number = models.CharField(max_length=20)
    clinical_interests = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
    ], use_json_field=True, blank=True)
    research_interests = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
    ], use_json_field=True, blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    consultation_info = StreamField([
        ('rich_text', RichTextBlock(label='Rich Text')),
        ('raw_html', RawHTMLBlock(label='Raw HTML')),
        ('content_block', ContentStreamBlock()),
    ], use_json_field=True, blank=True)
    is_active = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('specialization'),
            FieldPanel('qualification'),
            FieldPanel('experience_years'),
            FieldPanel('gmc_number'),
        ], heading="Professional Details"),
        FieldPanel('photo'),
        FieldPanel('clinical_interests'),
        FieldPanel('research_interests'),
        FieldPanel('consultation_info'),
        FieldPanel('is_active'),
        InlinePanel('weekly_schedules', label="Weekly Schedule")
    ]

    parent_page_types = ['hospital.DoctorIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctor Profiles"

    def get_available_slots(self, date):
        day_of_week = date.weekday()
        schedules = self.weekly_schedules.filter(
            day_of_week=day_of_week,
            is_available=True
        )
        available_slots = []
        for schedule in schedules:
            # Add logic here to check against appointments and return available time slots
            available_slots.append({
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'location': schedule.location,
                'clinic_type': schedule.clinic_type
            })
        return available_slots


class DoctorWeeklySchedule(models.Model):
    page = ParentalKey(DoctorPage, on_delete=models.CASCADE, related_name='weekly_schedules')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)
    clinic_type = models.CharField(max_length=100, blank=True)  # e.g., "General Clinic", "Specialist Clinic"

    panels = [
        FieldPanel('day_of_week'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('is_available'),
        FieldPanel('location'),
        FieldPanel('clinic_type'),
    ]

    class Meta:
        unique_together = ('page', 'day_of_week')
        ordering = ['day_of_week', 'start_time']


class HospitalLocationPage(Page):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    map_link = models.URLField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    facilities = RichTextField(blank=True)
    parking_info = RichTextField(blank=True)
    public_transport = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('map_link'),
        FieldPanel('image'),
        FieldPanel('facilities'),
        FieldPanel('parking_info'),
        FieldPanel('public_transport'),
    ]

    parent_page_types = ['hospital.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "Hospital Location"
        verbose_name_plural = "Hospital Locations"