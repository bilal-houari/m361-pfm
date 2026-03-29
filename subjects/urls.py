from django.urls import path
from .views import (
    SubjectListView, 
    SubjectCreateView, 
    SubjectUpdateView, 
    SubjectDeleteView
)

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('add/', SubjectCreateView.as_view(), name='subject-add'),
    path('edit/<int:pk>/', SubjectUpdateView.as_view(), name='subject-edit'),
    path('delete/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),
]
