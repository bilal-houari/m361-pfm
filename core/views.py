from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.role == 'STUDENT':
        return redirect('student-dashboard')
    return render(request, 'home.html')
