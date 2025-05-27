
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    UNIVERSITY_CHOICES = [
        ('TU_BERLIN', 'Technical University Berlin'),
        ('LMU_MUNICH', 'Ludwig Maximilian University Munich'),
        ('HEIDELBERG', 'University of Heidelberg'),
        ('TU_MUNICH', 'Technical University Munich'),
        ('HAMBURG', 'University of Hamburg'),
        ('FRANKFURT', 'Goethe University Frankfurt'),
        ('COLOGNE', 'University of Cologne'),
        ('Ilmenau', 'Technical University Ilmenau'),
        ('OTHER', 'Other')
    ]
    
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('IN', 'India'),
        ('CN', 'China'),
        ('BR', 'Brazil'),
        ('TR', 'Turkey'),
        ('RU', 'Russia'),
        ('MX', 'Mexico'),
        ('PK', 'PAKISTAN'),
        ('OTHER', 'Other')
    ]
    
    ARRIVAL_STATUS_CHOICES = [
        ('PLANNING', 'Planning to arrive'),
        ('ARRIVED', 'Already arrived'),
        ('RESIDING', 'Already residing in Germany')
    ]

    # Personal Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='OTHER')
    
    # Academic Information
    university = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    course_of_study = models.CharField(max_length=200, blank=True)
    expected_graduation = models.DateField(null=True, blank=True)
    
    # Location & Arrival Information
    intended_city = models.CharField(max_length=100, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    arrival_airport = models.CharField(max_length=10, blank=True)
    arrival_status = models.CharField(max_length=20, choices=ARRIVAL_STATUS_CHOICES, default='PLANNING')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile completion tracking
    profile_completed = models.BooleanField(default=False)
    registration_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"
