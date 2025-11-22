from django.urls import path
from . import views as api_views

urlpatterns = [
    # API UI Landing Page
    path('', api_views.api_dashboard, name='api_dashboard'),

    # Hospitals CRUD
    path('hospitals/', api_views.hospitals_list, name='hospitals_list'),
    path('hospitals/add/', api_views.hospital_create, name='hospital_create'),
    path('hospitals/edit/<int:pk>/', api_views.hospital_edit, name='hospital_edit'),
    path('hospitals/delete/<int:pk>/', api_views.hospital_delete, name='hospital_delete'),

    # Donors CRUD
    path('donors/', api_views.donors_list, name='donors_list'),
    path('donors/add/', api_views.donor_create, name='donor_create'),
    path('donors/edit/<int:pk>/', api_views.donor_edit, name='donor_edit'),
    path('donors/delete/<int:pk>/', api_views.donor_delete, name='donor_delete'),
]
