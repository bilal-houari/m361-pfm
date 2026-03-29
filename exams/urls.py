from django.urls import path
from .views import (
    ExamListView, 
    ExamCreateView, 
    ExamUpdateView, 
    ExamDeleteView,
    ExamResultEntryView
)

urlpatterns = [
    path('', ExamListView.as_view(), name='exam-list'),
    path('add/', ExamCreateView.as_view(), name='exam-add'),
    path('edit/<int:pk>/', ExamUpdateView.as_view(), name='exam-edit'),
    path('delete/<int:pk>/', ExamDeleteView.as_view(), name='exam-delete'),
    path('<int:pk>/results/', ExamResultEntryView.as_view(), name='exam-results'),
]
