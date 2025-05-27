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
        required=True
    )
    student_id = forms.CharField(max_length=50, required=False)
    course_of_study = forms.CharField(max_length=200, required=True)
    intended_city = forms.CharField(max_length=100, required=True)
    arrival_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    arrival_status = forms.ChoiceField(
        choices=CustomUser.ARRIVAL_STATUS_CHOICES,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
            'phone_number', 'date_of_birth', 'nationality', 'university', 'student_id',
            'course_of_study', 'intended_city', 'arrival_date', 'arrival_status'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = True

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
        user.intended_city = self.cleaned_data['intended_city']
        user.arrival_date = self.cleaned_data.get('arrival_date')
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