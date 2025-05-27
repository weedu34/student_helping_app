from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        # Create a sample student user
        if not User.objects.filter(username='student_test').exists():
            user = User.objects.create_user(
                username='student_test',
                email='student@example.com',
                password='testpass123',
                first_name='Max',
                last_name='Mustermann',
                phone_number='+49123456789',
                date_of_birth=date(1995, 5, 15),
                nationality='US',
                university='TU_BERLIN',
                student_id='12345678',
                course_of_study='Computer Science',
                intended_city='Berlin',
                arrival_date=date.today() + timedelta(days=30),
                arrival_status='PLANNING'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created test user: {user.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Test user already exists')
            )