# admin.py (for the accounts app)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'university', 'intended_city', 'arrival_status', 'is_staff']
    list_filter = ['university', 'intended_city', 'arrival_status', 'nationality', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'student_id']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Student Information', {
            'fields': ('phone_number', 'date_of_birth', 'nationality', 'university', 
                      'student_id', 'course_of_study', 'expected_graduation')
        }),
        ('Location & Arrival', {
            'fields': ('intended_city', 'arrival_date', 'arrival_airport', 'arrival_status')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Profile Status', {
            'fields': ('profile_completed', 'registration_completed')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'nationality', 
                      'university', 'course_of_study', 'intended_city')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)