# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=17, required=False)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    nationality = forms.ChoiceField(
        choices=CustomUser.COUNTRY_CHOICES,
        required=True
    )
    university = forms.ChoiceField(
        choices=CustomUser.UNIVERSITY_CHOICES,
        required=True,
        initial='TU_ILMENAU'
    )
    student_id = forms.CharField(max_length=50, required=False)
    course_of_study = forms.CharField(max_length=200, required=True)
    arrival_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="When do you plan to arrive in Ilmenau?"
    )
    arrival_airport = forms.CharField(
        max_length=50, 
        required=False,
        help_text="Which airport will you arrive at? (e.g., ERF-Erfurt, LEJ-Leipzig, FRA-Frankfurt)"
    )
    arrival_status = forms.ChoiceField(
        choices=CustomUser.ARRIVAL_STATUS_CHOICES,
        required=True,
        initial='PLANNING'
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
            'phone_number', 'date_of_birth', 'nationality', 'university', 'student_id',
            'course_of_study', 'arrival_date', 'arrival_airport', 'arrival_status'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = True
        
        # Add specific styling for certain fields
        self.fields['university'].widget.attrs['class'] += ' form-select'
        self.fields['nationality'].widget.attrs['class'] += ' form-select'
        self.fields['arrival_status'].widget.attrs['class'] += ' form-select'
        
        # Add placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'your.email@example.com'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = '+49 123 456 7890'
        self.fields['course_of_study'].widget.attrs['placeholder'] = 'e.g., Computer Science, Mechanical Engineering'
        self.fields['student_id'].widget.attrs['placeholder'] = 'Your student ID (if available)'
        self.fields['arrival_airport'].widget.attrs['placeholder'] = 'e.g., ERF, LEJ, FRA'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.nationality = self.cleaned_data['nationality']
        user.university = self.cleaned_data['university']
        user.student_id = self.cleaned_data.get('student_id', '')
        user.course_of_study = self.cleaned_data['course_of_study']
        user.intended_city = 'Ilmenau'  # Fixed to Ilmenau
        user.arrival_date = self.cleaned_data.get('arrival_date')
        user.arrival_airport = self.cleaned_data.get('arrival_airport', '')
        user.arrival_status = self.cleaned_data['arrival_status']
        
        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Allow login with email
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                return user.username
            except CustomUser.DoesNotExist:
                pass
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth',
            'course_of_study', 'student_id', 'arrival_date', 'arrival_airport',
            'arrival_status', 'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Add help text
        self.fields['phone_number'].help_text = 'Include country code (e.g., +49 for Germany)'
        self.fields['arrival_airport'].help_text = 'Main airports: ERF (Erfurt), LEJ (Leipzig), FRA (Frankfurt)'
        self.fields['emergency_contact_name'].help_text = 'Someone we can contact in case of emergency'
        self.fields['emergency_contact_phone'].help_text = 'Phone number with country code'