from django.urls import path
from . import views

urlpatterns = [
    path('', views.SchoolClassListView.as_view(), name='class-list'),
    path('add/', views.SchoolClassCreateView.as_view(), name='class-add'),
    path('<int:pk>/', views.SchoolClassDetailView.as_view(), name='class-detail'),
    path('<int:pk>/edit/', views.SchoolClassUpdateView.as_view(), name='class-edit'),
    path('<int:pk>/delete/', views.SchoolClassDeleteView.as_view(), name='class-delete'),
    
    # Assignments
    path('<int:class_pk>/assign/', views.ClassSubjectAssignmentCreateView.as_view(), name='class-assign'),
    path('assignment/<int:pk>/delete/', views.ClassSubjectAssignmentDeleteView.as_view(), name='assignment-delete'),
]
