from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
from teachers.models import Teacher
from admins.models import AdminProfile
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test accounts for Admin, Teacher, and Student'

    def handle(self, *args, **options):
        password = 'password'
        
        # Cleanup existing test users to ensure a fresh state
        test_emails = ['admin@preskool.com', 'teacher@preskool.com', 'student@preskool.com']
        User.objects.filter(email__in=test_emails).delete()
        User.objects.filter(username__in=test_emails).delete()
        
        # 1. Create Admin
        admin_user = User.objects.create_user(
            username='admin@preskool.com',
            email='admin@preskool.com',
            password=password,
            first_name='System',
            last_name='Administrator',
            role='ADMIN',
            is_staff=True,
            is_superuser=True
        )
        AdminProfile.objects.create(user=admin_user)
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin: {admin_user.email}'))

        # 2. Create Teacher
        teacher_user = User.objects.create_user(
            username='teacher@preskool.com',
            email='teacher@preskool.com',
            password=password,
            first_name='John',
            last_name='Doe',
            role='TEACHER'
        )
        Teacher.objects.create(
            user=teacher_user,
            date_of_birth=date(1985, 5, 20),
            specialization='Mathematics'
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created teacher: {teacher_user.email}'))

        # 3. Create Student
        student_user = User.objects.create_user(
            username='student@preskool.com',
            email='student@preskool.com',
            password=password,
            first_name='Jane',
            last_name='Smith',
            role='STUDENT'
        )
        Student.objects.create(
            user=student_user,
            admission_number='STU001',
            date_of_birth=date(2010, 10, 15),
            grade='10th Grade'
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created student: {student_user.email}'))
