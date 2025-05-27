# accounts/management/commands/populate_ilmenau_checklist.py

from django.core.management.base import BaseCommand
from accounts.models import IlmenauChecklistCategory, IlmenauChecklistItem, IlmenauResource

class Command(BaseCommand):
    help = 'Populate the database with Ilmenau-specific checklist items and resources'

    def handle(self, *args, **options):
        self.stdout.write('Populating Ilmenau checklist data...')
        
        # Clear existing data
        IlmenauChecklistItem.objects.all().delete()
        IlmenauChecklistCategory.objects.all().delete()
        IlmenauResource.objects.all().delete()
        
        # Create Categories specific to Ilmenau
        categories_data = [
            {
                'name': 'TU Ilmenau Preparation',
                'icon': 'fas fa-university',
                'description': 'Technical University of Ilmenau specific requirements',
                'order': 1
            },
            {
                'name': 'German Visa & Documents', 
                'icon': 'fas fa-passport',
                'description': 'Visa and document requirements for Germany',
                'order': 2
            },
            {
                'name': 'Travel to Ilmenau',
                'icon': 'fas fa-plane',
                'description': 'Getting to Ilmenau from major airports',
                'order': 3
            },
            {
                'name': 'Accommodation in Ilmenau',
                'icon': 'fas fa-home',
                'description': 'Finding and securing housing in Ilmenau',
                'order': 4
            },
            {
                'name': 'Financial Setup',
                'icon': 'fas fa-euro-sign',
                'description': 'Banking and financial arrangements in Germany',
                'order': 5
            },
            {
                'name': 'Health Insurance',
                'icon': 'fas fa-heart',
                'description': 'Mandatory health insurance for students in Germany',
                'order': 6
            },
            {
                'name': 'Life in Ilmenau',
                'icon': 'fas fa-city',
                'description': 'Preparing for daily life in Ilmenau',
                'order': 7
            },
            {
                'name': 'Essential Preparations',
                'icon': 'fas fa-suitcase',
                'description': 'Personal and practical preparations',
                'order': 8
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = IlmenauChecklistCategory.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'Created category: {category.name}')
        
        # Create Ilmenau-specific Checklist Items
        checklist_items = [
            # TU Ilmenau Preparation
            {
                'category': categories['TU Ilmenau Preparation'],
                'title': 'Confirm your admission to TU Ilmenau',
                'description': 'Verify your admission letter and complete enrollment process',
                'helpful_link': 'https://www.tu-ilmenau.de/en/',
                'link_text': 'TU Ilmenau International Students',
                'priority': 'high',
                'order': 1,
                'tu_ilmenau_specific': True
            },
            {
                'category': categories['TU Ilmenau Preparation'],
                'title': 'Register for courses at TU Ilmenau',
                'description': 'Complete your course registration through the university portal',
                'helpful_link': 'https://www.tu-ilmenau.de/en/international',
                'link_text': 'TU Ilmenau Study Portal',
                'priority': 'high',
                'order': 2,
                'tu_ilmenau_specific': True
            },
            {
                'category': categories['TU Ilmenau Preparation'],
                'title': 'Contact TU Ilmenau International Office',
                'description': 'Get in touch with the international office for guidance and support',
                'helpful_link': 'https://www.tu-ilmenau.de/en/international/',
                'link_text': 'TU Ilmenau International Office',
                'priority': 'medium',
                'order': 3,
                'tu_ilmenau_specific': True
            },
            
            # German Visa & Documents
            {
                'category': categories['German Visa & Documents'],
                'title': 'Apply for German student visa',
                'description': 'Apply for your student visa at the German consulate in your home country',
                'helpful_link': 'https://pakistan.diplo.de/pk-en/service/2-study-visa-seite-1676104',
                'link_text': 'German Visa Information',
                'priority': 'high',
                'order': 1
            },
            {
                'category': categories['German Visa & Documents'],
                'title': 'Prepare required documents',
                'description': 'Gather passport, admission letter, financial proof, health insurance, etc.',
                'helpful_link': 'https://www.study-in-germany.de/en/plan-your-studies/requirements/',
                'link_text': 'Required Documents Checklist',
                'priority': 'high',
                'order': 2
            },
            {
                'category': categories['German Visa & Documents'],
                'title': 'Get documents translated and certified',
                'description': 'Have important documents officially translated to German if required',
                'helpful_link': 'https://www.bdue.de/',
                'link_text': 'German Translators Association',
                'priority': 'medium',
                'order': 3
            },
            
            # Travel to Ilmenau
            {
                'category': categories['Travel to Ilmenau'],
                'title': 'Book flight to Germany',
                'description': 'Book flights to Frankfurt (FRA), Leipzig (LEJ), or Erfurt (ERF) airports',
                'helpful_link': 'https://www.skyscanner.com/',
                'link_text': 'Flight Search',
                'priority': 'high',
                'order': 1
            },
            {
                'category': categories['Travel to Ilmenau'],
                'title': 'Plan journey from airport to Ilmenau',
                'description': 'Research train/bus connections from your arrival airport to Ilmenau',
                'helpful_link': 'https://www.bahn.de/en',
                'link_text': 'Deutsche Bahn (German Railways)',
                'priority': 'high',
                'order': 2
            },
            {
                'category': categories['Travel to Ilmenau'],
                'title': 'Download German transport apps',
                'description': 'Install DB Navigator, MVV, and local transport apps',
                'helpful_link': 'https://www.bahn.de/service/mobile/db-navigator',
                'link_text': 'DB Navigator App',
                'priority': 'medium',
                'order': 3
            },
            
            # Accommodation in Ilmenau
            {
                'category': categories['Accommodation in Ilmenau'],
                'title': 'Apply for student dormitory',
                'description': 'Apply for accommodation through Studierendenwerk Thüringen',
                'helpful_link': 'https://www.stw-thueringen.de/en/housing/residential-homes.html',
                'link_text': 'Student Housing Ilmenau',
                'priority': 'high',
                'order': 1
            },
            {
                'category': categories['Accommodation in Ilmenau'],
                'title': 'Search for private accommodation',
                'description': 'Look for apartments or shared flats in Ilmenau if dorm is not available',
                'helpful_link': 'https://www.wg-gesucht.de/',
                'link_text': 'WG-Gesucht (Shared Flats)',
                'priority': 'high',
                'order': 2
            },
            {
                'category': categories['Accommodation in Ilmenau'],
                'title': 'Arrange temporary accommodation',
                'description': 'Book hotel/hostel for first few days while settling in',
                'helpful_link': 'https://www.booking.com/',
                'link_text': 'Booking.com',
                'priority': 'medium',
                'order': 3
            },
            
            # Financial Setup
            {
                'category': categories['Financial Setup'],
                'title': 'Research German banks in Ilmenau',
                'description': 'Compare banks like Sparkasse, Deutsche Bank, Commerzbank for student accounts',
                'helpful_link': 'https://www.google.com/maps/search/banks+ilmenau',
                'link_text': 'Sparkasse Ilmenau',
                'priority': 'high',
                'order': 1
            },
            {
                'category': categories['Financial Setup'],
                'title': 'Prepare financial documents',
                'description': 'Gather income proof, scholarship letters, blocked account details',
                'helpful_link': 'https://www.fintiba.com/',
                'link_text': 'Fintiba Blocked Account',
                'priority': 'high',
                'order': 2
            },
            {
                'category': categories['Financial Setup'],
                'title': 'Calculate monthly budget for Ilmenau',
                'description': 'Estimate costs for rent, food, transport, and other expenses in Ilmenau',
                'helpful_link': 'https://www.study-in-germany.de/en/plan-your-studies/costs-financing/',
                'link_text': 'Cost Calculator',
                'priority': 'medium',
                'order': 3
            },
            
            # Health Insurance
            {
                'category': categories['Health Insurance'],
                'title': 'Get German health insurance',
                'description': 'Arrange mandatory health insurance before arrival (AOK, TK, Barmer, etc.)',
                'helpful_link': 'https://www.tk.de/en',
                'link_text': 'Techniker Krankenkasse',
                'priority': 'high',
                'order': 1
            },
            {
                'category': categories['Health Insurance'],
                'title': 'Understand German healthcare system',
                'description': 'Learn about how healthcare works in Germany and finding doctors',
                'helpful_link': 'https://www.make-it-in-germany.com/en/living-in-germany/money-insurance/health-insurance',
                'link_text': 'Healthcare in Germany',
                'priority': 'medium',
                'order': 2
            },
            
            # Life in Ilmenau
            {
                'category': categories['Life in Ilmenau'],
                'title': 'Learn about Ilmenau city',
                'description': 'Research local culture, weather, and what to expect in Ilmenau',
                'helpful_link': 'https://www.ilmenau.de/',
                'link_text': 'City of Ilmenau Official Website',
                'priority': 'medium',
                'order': 1
            },
            {
                'category': categories['Life in Ilmenau'],
                'title': 'Find grocery stores and shopping',
                'description': 'Locate nearby supermarkets like REWE, EDEKA, Netto in Ilmenau',
                'helpful_link': 'https://www.google.com/maps/search/supermarket+ilmenau',
                'link_text': 'Supermarkets in Ilmenau',
                'priority': 'low',
                'order': 2
            },
            {
                'category': categories['Life in Ilmenau'],
                'title': 'Research local transportation',
                'description': 'Learn about buses and local transport in and around Ilmenau',
                'helpful_link': 'https://www.iov-ilmenau.de/',
                'link_text': 'Regional Transport',
                'priority': 'medium',
                'order': 3
            },
            
            # Essential Preparations
            {
                'category': categories['Essential Preparations'],
                'title': 'Pack for German weather',
                'description': 'Ilmenau can be cold - pack warm clothes and weather-appropriate items',
                'helpful_link': 'https://www.google.com/search?q=google+ilmenau+weather',
                'link_text': 'Ilmenau Weather Forecast',
                'priority': 'medium',
                'order': 1
            },
            
            {
                'category': categories['Essential Preparations'],
                'title': 'Learn basic German phrases',
                'description': 'Learn essential German words and phrases for daily communication',
                'helpful_link': 'https://www.duolingo.com/course/de/en',
                'link_text': 'Duolingo German Course',
                'priority': 'medium',
                'order': 3
            },
            {
                'category': categories['Essential Preparations'],
                'title': 'Emergency contacts and family notification',
                'description': 'Share your travel plans and Ilmenau contact details with family',
                'helpful_link': 'https://www.germany.travel/en/ms/visitor-info/important-numbers.html',
                'link_text': 'Emergency Numbers Germany',
                'priority': 'high',
                'order': 4
            }
        ]
        
        # Create all checklist items
        for item_data in checklist_items:
            IlmenauChecklistItem.objects.create(**item_data)
        
        # Create Ilmenau Resources
        resources_data = [
            # Transportation
            {
                'title': 'Deutsche Bahn (German Railways)',
                'description': 'Main railway service for traveling to and within Germany',
                'resource_type': 'transport',
                'website_url': 'https://www.bahn.de/en',
                'order': 1
            },
            {
                'title': 'Erfurt Airport (ERF)',
                'description': 'Closest major airport to Ilmenau (about 45 minutes by car)',
                'resource_type': 'transport',
                'website_url': 'https://www.flughafen-erfurt.de/',
                'order': 2
            },
            
            # Housing
            {
                'title': 'Studierendenwerk Thüringen',
                'description': 'Official student services for housing in Ilmenau',
                'resource_type': 'housing',
                'website_url': 'https://www.stw-thueringen.de/en/housing/ilmenau.html',
                'phone_number': '+49 3677 69-0',
                'order': 1
            },
            
            # University Services
            {
                'title': 'TU Ilmenau International Office',
                'description': 'Support for international students at Technical University',
                'resource_type': 'university',
                'website_url': 'https://www.tu-ilmenau.de/en/international/',
                'phone_number': '+49 3677 69-2520',
                'address': 'Ehrenbergstraße 29, 98693 Ilmenau',
                'order': 1
            },
            
            # Shopping
            {
                'title': 'REWE Ilmenau',
                'description': 'Major supermarket chain with locations in Ilmenau',
                'resource_type': 'shopping',
                'website_url': 'https://www.rewe.de/',
                'order': 1
            },
            
            # Emergency
            {
                'title': 'Emergency Services Germany',
                'description': 'Police: 110, Fire/Medical: 112',
                'resource_type': 'emergency',
                'phone_number': '110 (Police), 112 (Fire/Medical)',
                'order': 1
            }
        ]
        
        for resource_data in resources_data:
            IlmenauResource.objects.create(**resource_data)
        
        # Summary
        total_items = IlmenauChecklistItem.objects.count()
        total_resources = IlmenauResource.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {total_items} checklist items across {len(categories)} categories'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {total_resources} Ilmenau resources')
        )
        
        # Display summary
        for category in IlmenauChecklistCategory.objects.all():
            item_count = category.items.count()
            self.stdout.write(f'  - {category.name}: {item_count} items')
        
        self.stdout.write(
            self.style.SUCCESS('Ilmenau checklist population completed!')
        )