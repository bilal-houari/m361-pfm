from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student-list'),
    path('add/', views.StudentCreateView.as_view(), name='student-add'),
    path('edit/<int:pk>/', views.StudentUpdateView.as_view(), name='student-edit'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='student-delete'),
    
    # Student Interface
    path('dashboard/', views.StudentDashboardView.as_view(), name='student-dashboard'),
    path('results/', views.StudentExamResultsView.as_view(), name='student-results'),
    path('holidays-list/', views.StudentHolidayListView.as_view(), name='student-holidays'),
    path('my-class/', views.StudentClassListView.as_view(), name='student-class-list'),
]
