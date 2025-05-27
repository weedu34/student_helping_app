# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from .forms import StudentRegistrationForm, StudentLoginForm
from .models import CustomUser, IlmenauChecklistCategory, IlmenauChecklistItem, UserChecklistProgress, IlmenauResource


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
                messages.success(request, f'Welcome back, {user.get_full_name()}! Ready for your Ilmenau journey?')
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
            messages.success(request, 'Registration successful! Welcome to the Ilmenau Student Community!')
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
    
    # Get checklist data if user is planning to arrive
    checklist_data = None
    if user.arrival_status == 'PLANNING':
        checklist_data = get_user_ilmenau_checklist_data(user)
    
    context = {
        'user': user,
        'completion_percentage': calculate_profile_completion(user),
        'next_steps': get_next_steps(user),
        'checklist_data': checklist_data,
    }
    return render(request, 'accounts/dashboard.html', context)


def get_user_ilmenau_checklist_data(user):
    """Get organized Ilmenau checklist data for a user"""
    categories = IlmenauChecklistCategory.objects.prefetch_related('items').all()
    checklist_data = []
    
    total_items = 0
    completed_items = 0
    
    for category in categories:
        # Get relevant items for this user
        items = category.items.filter(is_active=True)
        relevant_items = [item for item in items if item.is_relevant_for_user(user)]
        
        # Get user's progress for these items
        item_progress = []
        for item in relevant_items:
            progress, created = UserChecklistProgress.objects.get_or_create(
                user=user,
                checklist_item=item,
                defaults={'is_completed': False}
            )
            item_progress.append({
                'item': item,
                'progress': progress,
                'is_completed': progress.is_completed
            })
            
            total_items += 1
            if progress.is_completed:
                completed_items += 1
        
        if relevant_items:  # Only include categories with relevant items
            checklist_data.append({
                'category': category,
                'items': item_progress,
                'completed_count': sum(1 for ip in item_progress if ip['is_completed']),
                'total_count': len(item_progress)
            })
    
    completion_percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
    
    return {
        'categories': checklist_data,
        'total_items': total_items,
        'completed_items': completed_items,
        'completion_percentage': completion_percentage
    }


@login_required
@require_http_methods(["POST"])
def toggle_checklist_item(request):
    """Toggle completion status of a checklist item via AJAX"""
    try:
        item_id = request.POST.get('item_id')
        is_completed = request.POST.get('is_completed') == 'true'
        notes = request.POST.get('notes', '')
        
        checklist_item = get_object_or_404(IlmenauChecklistItem, id=item_id)
        
        progress, created = UserChecklistProgress.objects.get_or_create(
            user=request.user,
            checklist_item=checklist_item,
            defaults={'is_completed': False}
        )
        
        progress.is_completed = is_completed
        progress.notes = notes
        if is_completed:
            progress.completed_date = timezone.now()
        else:
            progress.completed_date = None
        progress.save()
        
        # Calculate new completion percentage
        checklist_data = get_user_ilmenau_checklist_data(request.user)
        
        return JsonResponse({
            'success': True,
            'is_completed': progress.is_completed,
            'completion_percentage': checklist_data['completion_percentage']
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def checklist_view(request):
    """Dedicated checklist page for Ilmenau preparation"""
    if request.user.arrival_status != 'PLANNING':
        messages.info(request, 'Checklist is only available for users who are planning to arrive in Ilmenau.')
        return redirect('dashboard')
    
    checklist_data = get_user_ilmenau_checklist_data(request.user)
    
    context = {
        'checklist_data': checklist_data,
        'user': request.user
    }
    return render(request, 'accounts/checklist.html', context)


@login_required
def ilmenau_resources(request):
    """View for Ilmenau-specific resources"""
    resources_by_type = {}
    
    for resource in IlmenauResource.objects.filter(is_active=True).order_by('resource_type', 'order'):
        resource_type = resource.get_resource_type_display()
        if resource_type not in resources_by_type:
            resources_by_type[resource_type] = []
        resources_by_type[resource_type].append(resource)
    
    context = {
        'resources_by_type': resources_by_type,
        'user': request.user
    }
    return render(request, 'accounts/ilmenau_resources.html', context)


def get_next_steps(user):
    """Get personalized next steps for Ilmenau students"""
    steps = []
    
    if user.arrival_status == 'PLANNING':
        # Get top priority incomplete checklist items specific to Ilmenau
        incomplete_high_priority = UserChecklistProgress.objects.filter(
            user=user,
            is_completed=False,
            checklist_item__priority='high',
            checklist_item__is_active=True
        ).select_related('checklist_item')[:3]
        
        for progress in incomplete_high_priority:
            item = progress.checklist_item
            steps.append({
                'title': item.title,
                'description': item.description,
                'priority': 'high',
                'link': item.helpful_link,
                'link_text': item.link_text
            })
        
        # Add profile completion if not done
        if not user.phone_number:
            steps.append({
                'title': 'Complete Your Profile',
                'description': 'Add your phone number and emergency contact information',
                'priority': 'medium'
            })
        
        # Add Ilmenau-specific suggestions if no high priority items
        if not incomplete_high_priority:
            steps.append({
                'title': 'Apply for Student Dormitory',
                'description': 'Apply for accommodation through Studierendenwerk Thüringen',
                'priority': 'high',
                'link': 'https://www.stw-thueringen.de/en/housing/ilmenau.html',
                'link_text': 'Student Housing Ilmenau'
            })
    
    elif user.arrival_status == 'ARRIVED':
        # Post-arrival steps specific to Ilmenau
        if not user.registration_completed:
            steps.append({
                'title': 'Complete Ilmenau City Registration (Anmeldung)',
                'description': 'Register your address with Ilmenau city authorities within 14 days of arrival',
                'priority': 'high',
                'link': 'https://www.ilmenau.de/',
                'link_text': 'Ilmenau City Registration'
            })
        
        steps.append({
            'title': 'Open Bank Account in Ilmenau',
            'description': 'Visit Sparkasse Ilmenau or other local banks to open a student account',
            'priority': 'high',
            'link': 'https://www.sparkasse-arnstadt-ilmenau.de/',
            'link_text': 'Sparkasse Ilmenau'
        })
        
        if user.university == 'TU_ILMENAU':
            steps.append({
                'title': 'Visit TU Ilmenau International Office',
                'description': 'Complete your enrollment and get your student ID card',
                'priority': 'high',
                'link': 'https://www.tu-ilmenau.de/en/international/',
                'link_text': 'TU Ilmenau International Office'
            })
        
        steps.append({
            'title': 'Get Local Phone Plan',
            'description': 'Set up a German mobile phone plan for better connectivity',
            'priority': 'medium',
            'link': 'https://www.telekom.de/en',
            'link_text': 'Deutsche Telekom'
        })
    
    return steps


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


@login_required
def user_list(request):
    """Display list of all Ilmenau students with search and filter functionality"""
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(university__icontains=search_query) |
            Q(course_of_study__icontains=search_query)
        )
    
    # Filter by university
    university_filter = request.GET.get('university', '')
    if university_filter:
        users = users.filter(university=university_filter)
    
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
    statuses = CustomUser.ARRIVAL_STATUS_CHOICES
    
    context = {
        'users': users_page,
        'search_query': search_query,
        'university_filter': university_filter,
        'status_filter': status_filter,
        'universities': universities,
        'statuses': statuses,
        'total_users': users.count(),
    }
    
    return render(request, 'accounts/user_list.html', context)


@login_required
def user_detail(request, user_id):
    """Display detailed information about a specific Ilmenau student"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Only allow users to view their own profile or staff to view all
    if not request.user.is_staff and request.user != user:
        messages.error(request, "You don't have permission to view this profile.")
        return redirect('dashboard')
    
    # Get checklist progress if user is planning
    checklist_progress = None
    if user.arrival_status == 'PLANNING':
        checklist_progress = get_user_ilmenau_checklist_data(user)
    
    context = {
        'profile_user': user,
        'completion_percentage': calculate_profile_completion(user),
        'checklist_progress': checklist_progress,
    }
    
    return render(request, 'accounts/user_detail.html', context)


def calculate_profile_completion(user):
    """Calculate profile completion percentage"""
    total_fields = 11  # Reduced since intended_city is fixed
    completed_fields = 0
    
    if user.first_name: completed_fields += 1
    if user.last_name: completed_fields += 1
    if user.email: completed_fields += 1
    if user.phone_number: completed_fields += 1
    if user.date_of_birth: completed_fields += 1
    if user.nationality: completed_fields += 1
    if user.university: completed_fields += 1
    if user.course_of_study: completed_fields += 1
    if user.arrival_date: completed_fields += 1
    if user.emergency_contact_name: completed_fields += 1
    if user.emergency_contact_phone: completed_fields += 1
    
    return int((completed_fields / total_fields) * 100)