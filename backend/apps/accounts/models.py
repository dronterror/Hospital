from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('staff', 'Staff'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = PhoneNumberField(blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'user_type']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})" 