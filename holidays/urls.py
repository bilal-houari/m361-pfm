from django.urls import path
from .views import (
    HolidayListView, 
    HolidayCreateView, 
    HolidayUpdateView, 
    HolidayDeleteView
)

urlpatterns = [
    path('', HolidayListView.as_view(), name='holiday-list'),
    path('add/', HolidayCreateView.as_view(), name='holiday-add'),
    path('edit/<int:pk>/', HolidayUpdateView.as_view(), name='holiday-edit'),
    path('delete/<int:pk>/', HolidayDeleteView.as_view(), name='holiday-delete'),
]
