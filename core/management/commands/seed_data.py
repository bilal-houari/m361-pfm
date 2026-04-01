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
from classes.models import SchoolClass, ClassSubjectAssignment

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
                classes = self.create_classes(teachers, subjects)
                students = self.create_students(classes)
                self.create_holidays()
                self.create_exams_and_results(subjects, students, classes)
                
            self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Seeding failed: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

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

        for _ in range(29): # More teachers to cover all subjects
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
        self.stdout.write(f'  - {len(teachers)} Teachers created')
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
        
        # Track which teachers have been assigned to subjects
        unassigned_teachers = [t for t in teachers if t != main_teacher]
        
        for dept in departments:
            names = subject_data.get(dept.name, [f"{dept.name} 101"])
            for name in names:
                code = f"{dept.name[:3].upper()}-{fake.unique.random_number(digits=3)}"
                subject = Subject.objects.create(
                    name=name,
                    code=code,
                    department=dept
                )
                
                # Assign teacher@preskool.com to Geometry specifically
                if name == 'Geometry' and main_teacher.subject is None:
                    main_teacher.subject = subject
                    main_teacher.save()
                
                # Each subject gets at least 1-2 teachers
                # Assign unassigned teachers first
                for _ in range(2):
                    if unassigned_teachers:
                        teacher = unassigned_teachers.pop(0)
                        teacher.subject = subject
                        teacher.save()
                
                subjects.append(subject)
        
        # Fallback if Geometry wasn't found for some reason
        if main_teacher.subject is None:
            main_teacher.subject = random.choice(subjects)
            main_teacher.save()
            
        self.stdout.write(f'  - {len(subjects)} Subjects created and teachers assigned')
        return subjects

    def create_classes(self, teachers, subjects):
        classes = []
        grade_levels = range(1, 11) # Grades 1-10
        
        main_teacher = next(t for t in teachers if t.user.email == 'teacher@preskool.com')
        
        for level in grade_levels:
            name = f"Grade {level}"
            school_class = SchoolClass.objects.create(
                name=name,
                grade_level=level
            )
            
            # Pick other random subjects
            available_subjects = [s for s in subjects if s != main_teacher.subject]
            class_subjects = random.sample(available_subjects, k=random.randint(4, 7))
            
            # ALWAYS include the main teacher's subject in every class to ensure they have load
            class_subjects.append(main_teacher.subject)
            
            # For each subject, assign ONE teacher specializing in it
            for subject in class_subjects:
                if subject == main_teacher.subject:
                    # Always assign main teacher to their subject
                    teacher = main_teacher
                else:
                    # Strictly filter teachers who actually teach this subject
                    subject_teachers = list(Teacher.objects.filter(subject=subject))
                    if not subject_teachers:
                        # If no specialist, pick a teacher from the same department
                        subject_teachers = list(Teacher.objects.filter(subject__department=subject.department))
                    
                    if not subject_teachers:
                        # Final fallback: any teacher
                        teacher = random.choice(teachers)
                    else:
                        teacher = random.choice(subject_teachers)

                ClassSubjectAssignment.objects.create(
                    school_class=school_class,
                    subject=subject,
                    teacher=teacher
                )
            
            classes.append(school_class)
        
        self.stdout.write(f'  - {len(classes)} Classes created with subject assignments')
        return classes

    def create_students(self, classes):
        students = []
        
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
        
        # Grade 8 for main student
        class_8 = next(c for c in classes if c.name == 'Grade 8')
        main_student = Student.objects.create(
            user=main_user,
            admission_number='ADM10001',
            date_of_birth=fake.date_of_birth(minimum_age=13, maximum_age=14),
            school_class=class_8,
            address=fake.address(),
            phone_number=fake.phone_number()[:15]
        )
        students.append(main_student)

        for _ in range(199): # Total students = 200
            email = fake.unique.email()
            user = CustomUser.objects.create_user(
                email=email,
                username=email,
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='STUDENT'
            )
            
            # Weighted random choice or just random choice for distribution
            student_class = random.choice(classes)
            
            student = Student.objects.create(
                user=user,
                admission_number=f"ADM{fake.unique.random_number(digits=5)}",
                date_of_birth=fake.date_of_birth(minimum_age=6, maximum_age=17),
                school_class=student_class,
                address=fake.address(),
                phone_number=fake.phone_number()[:15]
            )
            students.append(student)
        
        self.stdout.write(f'  - {len(students)} Students created (including student@preskool.com in {class_8.name})')
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

    def create_exams_and_results(self, subjects, students, classes):
        exam_names = ['Mid-Term Exam', 'Final Exam', 'Monthly Quiz']
        today = timezone.now().date()
        
        main_student = next(s for s in students if s.user.email == 'student@preskool.com')
        
        exam_count = 0
        result_count = 0
        
    def create_exams_and_results(self, subjects, students, classes):
        exam_names = ['Mid-Term Exam', 'Final Exam', 'Monthly Quiz']
        today = timezone.now().date()
        
        exam_count = 0
        result_count = 0
        
        # For each class, manage exams for their assigned subjects
        for school_class in classes:
            class_assignments = list(school_class.assignments.all())
            if not class_assignments:
                continue
                
            # Fetch students in this class once
            class_students = [s for s in students if s.school_class == school_class]
            if not class_students:
                continue

            for assignment in class_assignments:
                # Create a set of exams for this specific class and subject
                for i, exam_name in enumerate(exam_names):
                    exam = Exam.objects.create(
                        name=f"{school_class.name} - {exam_name}",
                        date=today - timedelta(days=random.randint(10, 60)),
                        subject=assignment.subject,
                        school_class=school_class,
                        max_marks=random.choice([50, 100])
                    )
                    exam_count += 1
                    
                    # Detect if this is the "last" exam (e.g. the Monthly Quiz)
                    # to simulate unfinished grading (20% graded)
                    is_last_exam = (i == len(exam_names) - 1)
                    
                    if is_last_exam:
                        # Only 20% of students get a result
                        graded_students = random.sample(class_students, k=max(1, int(len(class_students) * 0.2)))
                    else:
                        # All students get a result
                        graded_students = class_students

                    for student in graded_students:
                        ExamResult.objects.create(
                            exam=exam,
                            student=student,
                            marks_obtained=random.uniform(exam.max_marks * 0.4, exam.max_marks)
                        )
                        result_count += 1
                    
        self.stdout.write(f'  - {exam_count} Exams and {result_count} Exam Results created (highly class-aware + partial grading)')
