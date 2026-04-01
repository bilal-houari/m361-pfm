from django.urls import path
from .views import (
    TeacherListView, 
    TeacherCreateView, 
    TeacherUpdateView, 
    TeacherDeleteView,
    TeacherDashboardView,
    TeacherClassListView,
    TeacherClassDetailView,
    TeacherDepartmentView
)

urlpatterns = [
    path('dashboard/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('my-classes/', TeacherClassListView.as_view(), name='teacher-class-list'),
    path('my-classes/<int:pk>/', TeacherClassDetailView.as_view(), name='teacher-class-detail'),
    path('my-department/', TeacherDepartmentView.as_view(), name='teacher-department'),
    
    path('', TeacherListView.as_view(), name='teacher-list'),
    path('add/', TeacherCreateView.as_view(), name='teacher-add'),
    path('edit/<int:pk>/', TeacherUpdateView.as_view(), name='teacher-edit'),
    path('delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher-delete'),
]
