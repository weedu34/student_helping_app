# views.py
from django.shortcuts import render, redirect, get_object_or_404  # Added get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator  # Added for pagination
from django.db.models import Q  # Added for search functionality
from .forms import StudentRegistrationForm, StudentLoginForm
from .models import CustomUser

def student_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def student_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def student_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'completion_percentage': calculate_profile_completion(user),
        'next_steps': get_next_steps(user),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        # Handle profile updates
        user = request.user
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.emergency_contact_name = request.POST.get('emergency_contact_name', user.emergency_contact_name)
        user.emergency_contact_phone = request.POST.get('emergency_contact_phone', user.emergency_contact_phone)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
    
    return render(request, 'accounts/profile_update.html', {'user': request.user})


# NEW VIEWS - ADD THESE
@login_required
def user_list(request):
    """Display list of all users with search and filter functionality"""
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(intended_city__icontains=search_query) |
            Q(university__icontains=search_query)
        )
    
    # Filter by university
    university_filter = request.GET.get('university', '')
    if university_filter:
        users = users.filter(university=university_filter)
    
    # Filter by city
    city_filter = request.GET.get('city', '')
    if city_filter:
        users = users.filter(intended_city__icontains=city_filter)
    
    # Filter by arrival status
    status_filter = request.GET.get('status', '')
    if status_filter:
        users = users.filter(arrival_status=status_filter)
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    # Get filter options for dropdowns
    universities = CustomUser.objects.values_list('university', flat=True).distinct()
    cities = CustomUser.objects.values_list('intended_city', flat=True).distinct()
    statuses = CustomUser.ARRIVAL_STATUS_CHOICES
    
    context = {
        'users': users_page,
        'search_query': search_query,
        'university_filter': university_filter,
        'city_filter': city_filter,
        'status_filter': status_filter,
        'universities': universities,
        'cities': cities,
        'statuses': statuses,
        'total_users': users.count(),
    }
    
    return render(request, 'accounts/user_list.html', context)


@login_required
def user_detail(request, user_id):
    """Display detailed information about a specific user"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Only allow users to view their own profile or staff to view all
    if not request.user.is_staff and request.user != user:
        messages.error(request, "You don't have permission to view this profile.")
        return redirect('dashboard')
    
    context = {
        'profile_user': user,
        'completion_percentage': calculate_profile_completion(user),
    }
    
    return render(request, 'accounts/user_detail.html', context)


# EXISTING HELPER FUNCTIONS
def calculate_profile_completion(user):
    """Calculate profile completion percentage"""
    total_fields = 12
    completed_fields = 0
    
    if user.first_name: completed_fields += 1
    if user.last_name: completed_fields += 1
    if user.email: completed_fields += 1
    if user.phone_number: completed_fields += 1
    if user.date_of_birth: completed_fields += 1
    if user.nationality: completed_fields += 1
    if user.university: completed_fields += 1
    if user.course_of_study: completed_fields += 1
    if user.intended_city: completed_fields += 1
    if user.arrival_date: completed_fields += 1
    if user.emergency_contact_name: completed_fields += 1
    if user.emergency_contact_phone: completed_fields += 1
    
    return int((completed_fields / total_fields) * 100)


def get_next_steps(user):
    """Get personalized next steps for the user"""
    steps = []
    
    if not user.registration_completed:
        steps.append({
            'title': 'Complete City Registration (Anmeldung)',
            'description': 'Register your address with local authorities within 14 days',
            'priority': 'high'
        })
    
    if not user.phone_number:
        steps.append({
            'title': 'Get German Phone Number',
            'description': 'Get a local phone number for better connectivity',
            'priority': 'medium'
        })
    
    if user.arrival_status == 'PLANNING':
        steps.append({
            'title': 'Plan Airport Transportation',
            'description': f'Plan your route from {user.arrival_airport} to {user.intended_city}',
            'priority': 'high'
        })
    
    return steps