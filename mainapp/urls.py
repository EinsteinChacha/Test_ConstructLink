from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('marketplace/', views.equipment_marketplace, name='equipment_marketplace'),
    path('marketplace/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/equipment-owner/', views.equipment_owner_dashboard, name='equipment_owner_dashboard'),
    path('dashboard/contractor/', views.contractor_dashboard, name='contractor_dashboard'),
    path('dashboard/driver/', views.driver_dashboard, name='driver_dashboard'),
    path('dashboard/logistics-partner/', views.logistics_partner_dashboard, name='logistics_partner_dashboard'),
    path('dashboard/construction-company/', views.construction_company_dashboard, name='construction_company_dashboard'),
    path('dashboard/individual-client/', views.individual_client_dashboard, name='individual_client_dashboard'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
]
