# models.py - Simplified for Ilmenau focus

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Simplified to focus only on Ilmenau
    UNIVERSITY_CHOICES = [
        ('TU_ILMENAU', 'Technical University of Ilmenau'),
        ('OTHER_ILMENAU', 'Other Institution in Ilmenau'),
    ]
    
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('IN', 'India'),
        ('CN', 'China'),
        ('BR', 'Brazil'),
        ('TR', 'Turkey'),
        ('RU', 'Russia'),
        ('MX', 'Mexico'),
        ('PK', 'Pakistan'),
        ('BD', 'Bangladesh'),
        ('NG', 'Nigeria'),
        ('OTHER', 'Other')
    ]
    
    # Simplified ARRIVAL_STATUS_CHOICES - Only 2 options
    ARRIVAL_STATUS_CHOICES = [
        ('PLANNING', 'Planning to Arrive in Ilmenau'),
        ('ARRIVED', 'Arrived in Ilmenau'),
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
    university = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, default='TU_ILMENAU')
    student_id = models.CharField(max_length=50, blank=True)
    course_of_study = models.CharField(max_length=200, blank=True)
    expected_graduation = models.DateField(null=True, blank=True)
    
    # Location & Arrival Information (Fixed to Ilmenau)
    intended_city = models.CharField(max_length=100, default='Ilmenau', editable=False)
    arrival_date = models.DateField(null=True, blank=True)
    arrival_airport = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Main airports: ERF (Erfurt), LEJ (Leipzig), FRA (Frankfurt)"
    )
    arrival_status = models.CharField(max_length=20, choices=ARRIVAL_STATUS_CHOICES, default='PLANNING')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile completion tracking
    profile_completed = models.BooleanField(default=False)
    registration_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()} ({self.get_university_display()})"
    
    def get_checklist_completion_percentage(self):
        """Calculate completion percentage for planning checklist"""
        if self.arrival_status == 'PLANNING':
            total_items = IlmenauChecklistItem.objects.filter(is_active=True).count()
            if total_items == 0:
                return 0
            completed_items = UserChecklistProgress.objects.filter(
                user=self, 
                is_completed=True
            ).count()
            return int((completed_items / total_items) * 100) if total_items > 0 else 0
        return 100  # If arrived, checklist is considered complete


class IlmenauChecklistCategory(models.Model):
    """Categories for Ilmenau-specific checklist items"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Ilmenau Checklist Categories"
    
    def __str__(self):
        return f"Ilmenau: {self.name}"


class IlmenauChecklistItem(models.Model):
    """Checklist items specifically for coming to Ilmenau"""
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]
    
    category = models.ForeignKey(IlmenauChecklistCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    helpful_link = models.URLField(blank=True, help_text="Helpful web link for this task")
    link_text = models.CharField(max_length=100, blank=True, help_text="Display text for the link")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Specific to TU Ilmenau or general Ilmenau
    tu_ilmenau_specific = models.BooleanField(default=False, help_text="Only for TU Ilmenau students")
    
    class Meta:
        ordering = ['category__order', 'order']
        verbose_name = "Ilmenau Checklist Item"
        verbose_name_plural = "Ilmenau Checklist Items"
    
    def __str__(self):
        prefix = "[TU] " if self.tu_ilmenau_specific else "[General] "
        return f"{prefix}{self.category.name}: {self.title}"
    
    def is_relevant_for_user(self, user):
        """Check if this item is relevant for the specific user"""
        if self.tu_ilmenau_specific and user.university != 'TU_ILMENAU':
            return False
        return True


class UserChecklistProgress(models.Model):
    """Track individual user's progress on Ilmenau checklist items"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='checklist_progress_items')
    checklist_item = models.ForeignKey(IlmenauChecklistItem, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="User's personal notes for this item")
    
    class Meta:
        unique_together = ['user', 'checklist_item']
        verbose_name = "User Checklist Progress"
        verbose_name_plural = "User Checklist Progress"
    
    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.user.username}: {self.checklist_item.title}"


# Ilmenau-specific resources model
class IlmenauResource(models.Model):
    """Important resources and information for Ilmenau"""
    RESOURCE_TYPES = [
        ('transport', 'Transportation'),
        ('housing', 'Housing'),
        ('shopping', 'Shopping'),
        ('healthcare', 'Healthcare'),
        ('university', 'University Services'),
        ('government', 'Government Services'),
        ('social', 'Social & Recreation'),
        ('emergency', 'Emergency Contacts'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    website_url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['resource_type', 'order']
    
    def __str__(self):
        return f"{self.get_resource_type_display()}: {self.title}"