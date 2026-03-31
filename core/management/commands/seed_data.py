import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from faker import Faker

from users.models import CustomUser
from students.models import Student
from teachers.models import Teacher
from admins.models import AdminProfile
from departments.models import Department
from subjects.models import Subject
from holidays.models import Holiday
from exams.models import Exam, ExamResult

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with realistic data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        try:
            with transaction.atomic():
                self.create_admin()
                departments = self.create_departments()
                teachers = self.create_teachers(departments)
                subjects = self.create_subjects(departments, teachers)
                students = self.create_students()
                self.create_holidays()
                self.create_exams_and_results(subjects, students)
                
            self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Seeding failed: {e}'))

    def create_admin(self):
        admin_email = 'admin@preskool.com'
        if not CustomUser.objects.filter(email=admin_email).exists():
            admin_user = CustomUser.objects.create_superuser(
                email=admin_email,
                username=admin_email,
                password='password',
                first_name='System',
                last_name='Administrator',
                role='ADMIN'
            )
            AdminProfile.objects.create(
                user=admin_user,
                phone_number=fake.phone_number()[:15],
                address=fake.address()
            )
            self.stdout.write('  - Admin (Superuser) created')

    def create_departments(self):
        dept_names = ['Mathematics', 'Science', 'Languages', 'Arts', 'Physical Education', 'Computer Science']
        departments = []
        for name in dept_names:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'description': fake.text(max_nb_chars=200)}
            )
            departments.append(dept)
        self.stdout.write(f'  - {len(departments)} Departments created')
        return departments

    def create_teachers(self, departments):
        teachers = []
        # Main Teacher
        main_teacher_email = 'teacher@preskool.com'
        main_user = CustomUser.objects.create_user(
            email=main_teacher_email,
            username=main_teacher_email,
            password='password',
            first_name='Main',
            last_name='Teacher',
            role='TEACHER'
        )
        main_teacher = Teacher.objects.create(
            user=main_user,
            date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=50),
            specialization='General Education',
            address=fake.address(),
            phone_number=fake.phone_number()[:15]
        )
        teachers.append(main_teacher)

        for _ in range(11):
            email = fake.unique.email()
            user = CustomUser.objects.create_user(
                email=email,
                username=email,
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='TEACHER'
            )
            teacher = Teacher.objects.create(
                user=user,
                date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=60),
                specialization=fake.job()[:100],
                address=fake.address(),
                phone_number=fake.phone_number()[:15]
            )
            teachers.append(teacher)
        self.stdout.write(f'  - {len(teachers)} Teachers created (including teacher@preskool.com)')
        return teachers

    def create_subjects(self, departments, teachers):
        subjects = []
        subject_data = {
            'Mathematics': ['Algebra', 'Geometry', 'Calculus'],
            'Science': ['Physics', 'Chemistry', 'Biology'],
            'Languages': ['English', 'French', 'Spanish'],
            'Arts': ['History', 'Geography', 'Fine Arts'],
            'Physical Education': ['Sports', 'Yoga'],
            'Computer Science': ['Programming', 'Networking', 'Web Dev']
        }
        
        main_teacher = next(t for t in teachers if t.user.email == 'teacher@preskool.com')
        
        for dept in departments:
            names = subject_data.get(dept.name, [f"{dept.name} 101"])
            for name in names:
                code = f"{dept.name[:3].upper()}-{fake.unique.random_number(digits=3)}"
                subject = Subject.objects.create(
                    name=name,
                    code=code,
                    department=dept
                )
                
                # Assign main teacher to at least 4 subjects across different departments
                if len(subjects) % 4 == 0:
                    subject.teachers.add(main_teacher)
                
                assigned_teachers = random.sample(teachers, k=random.randint(1, 2))
                subject.teachers.add(*assigned_teachers)
                subjects.append(subject)
        
        self.stdout.write(f'  - {len(subjects)} Subjects created (teacher@preskool.com assigned to several)')
        return subjects

    def create_students(self):
        students = []
        grades = [f"Grade {i}" for i in range(1, 11)]
        
        # Main Student
        main_student_email = 'student@preskool.com'
        main_user = CustomUser.objects.create_user(
            email=main_student_email,
            username=main_student_email,
            password='password',
            first_name='Main',
            last_name='Student',
            role='STUDENT'
        )
        main_student = Student.objects.create(
            user=main_user,
            admission_number='ADM10001',
            date_of_birth=fake.date_of_birth(minimum_age=12, maximum_age=15),
            grade='Grade 8',
            address=fake.address(),
            phone_number=fake.phone_number()[:15]
        )
        students.append(main_student)

        for _ in range(59):
            email = fake.unique.email()
            user = CustomUser.objects.create_user(
                email=email,
                username=email,
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='STUDENT'
            )
            student = Student.objects.create(
                user=user,
                admission_number=f"ADM{fake.unique.random_number(digits=5)}",
                date_of_birth=fake.date_of_birth(minimum_age=6, maximum_age=17),
                grade=random.choice(grades),
                address=fake.address(),
                phone_number=fake.phone_number()[:15]
            )
            students.append(student)
        
        self.stdout.write(f'  - {len(students)} Students created (including student@preskool.com)')
        return students

    def create_holidays(self):
        h_names = ['New Year', 'Spring Break', 'Summer Vacation', 'Independence Day', 'Winter Break']
        today = timezone.now().date()
        
        for name in h_names:
            start_date = today + timedelta(days=random.randint(10, 300))
            Holiday.objects.create(
                name=name,
                start_date=start_date,
                end_date=start_date + timedelta(days=random.randint(1, 15)),
                description=fake.catch_phrase()
            )
        self.stdout.write(f'  - {len(h_names)} Holidays created')

    def create_exams_and_results(self, subjects, students):
        exam_names = ['Mid-Term Exam', 'Final Exam', 'Monthly Quiz']
        today = timezone.now().date()
        
        main_student = next(s for s in students if s.user.email == 'student@preskool.com')
        
        exam_count = 0
        result_count = 0
        
        # Create some exams for random subjects
        for exam_name in exam_names:
            sampled_subjects = subjects # Create exams for ALL subjects for variety
            for subject in sampled_subjects:
                exam = Exam.objects.create(
                    name=f"{exam_name} - {subject.name}",
                    date=today - timedelta(days=random.randint(10, 60)), # Recent exams
                    subject=subject,
                    max_marks=random.choice([50, 100])
                )
                exam_count += 1
                
                # Always assign a result to the main student
                ExamResult.objects.create(
                    exam=exam,
                    student=main_student,
                    marks_obtained=random.uniform(exam.max_marks * 0.5, exam.max_marks) # Always passing
                )
                result_count += 1
                
                # Assign results to 15-20 other random students
                other_students = [s for s in students if s != main_student]
                sampled_students = random.sample(other_students, k=random.randint(10, 15))
                for student in sampled_students:
                    ExamResult.objects.create(
                        exam=exam,
                        student=student,
                        marks_obtained=random.uniform(exam.max_marks * 0.3, exam.max_marks)
                    )
                    result_count += 1
                    
        self.stdout.write(f'  - {exam_count} Exams and {result_count} Exam Results created (student@preskool.com has all results)')
