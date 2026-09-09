from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_home, name='public_home'),
    path('cars/', views.public_cars, name='public_cars'),
    path('cars/<slug:slug>/', views.public_car_detail, name='public_car_detail'),
    path('about/', views.public_about, name='public_about'),
    path('contact/', views.public_contact, name='public_contact'),
]
