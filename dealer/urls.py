from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.dealer_login, name='dealer_login'),
    path('logout/', views.dealer_logout, name='dealer_logout'),
    path('dashboard/', views.dealer_dashboard, name='dealer_dashboard'),

    # Cars CRUD
    path('cars/', views.dealer_car_list, name='dealer_car_list'),
    path('cars/add/', views.dealer_car_create, name='dealer_car_create'),
    path('cars/<int:pk>/', views.dealer_car_detail, name='dealer_car_detail'),
    path('cars/<int:pk>/edit/', views.dealer_car_edit, name='dealer_car_edit'),
    path('cars/<int:pk>/delete/', views.dealer_car_delete, name='dealer_car_delete'),

    # Advertisements CRUD
    path('advertisements/', views.dealer_ad_list, name='dealer_ad_list'),
    path('advertisements/add/', views.dealer_ad_create, name='dealer_ad_create'),
    path('advertisements/<int:pk>/edit/', views.dealer_ad_edit, name='dealer_ad_edit'),
    path('advertisements/<int:pk>/delete/', views.dealer_ad_delete, name='dealer_ad_delete'),

    # Enquiries
    path('enquiries/', views.dealer_enquiry_list, name='dealer_enquiry_list'),
    path('enquiries/<int:pk>/', views.dealer_enquiry_detail, name='dealer_enquiry_detail'),

    # Settings
    path('settings/', views.dealer_settings_edit, name='dealer_settings_edit'),
]
