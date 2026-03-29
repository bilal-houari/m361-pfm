from django.urls import path
from .views import (
    StudentListView, 
    StudentCreateView, 
    StudentUpdateView, 
    StudentDeleteView
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('add/', StudentCreateView.as_view(), name='student-add'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student-edit'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
]
