from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from departments.models import Department
from classes.models import SchoolClass

@login_required
def home(request):
    if request.user.role == 'STUDENT':
        return redirect('student-dashboard')
    elif request.user.role == 'TEACHER':
        return redirect('teacher-dashboard')
    
    context = {
        'student_count': Student.objects.count(),
        'teacher_count': Teacher.objects.count(),
        'dept_count': Department.objects.count(),
        'class_count': SchoolClass.objects.count(),
    }
    return render(request, 'home.html', context)
