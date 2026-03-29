from django.urls import path
from .views import (
    DepartmentListView, 
    DepartmentCreateView, 
    DepartmentUpdateView, 
    DepartmentDeleteView
)

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department-list'),
    path('add/', DepartmentCreateView.as_view(), name='department-add'),
    path('edit/<int:pk>/', DepartmentUpdateView.as_view(), name='department-edit'),
    path('delete/<int:pk>/', DepartmentDeleteView.as_view(), name='department-delete'),
]
