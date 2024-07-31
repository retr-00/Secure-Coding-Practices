from django.urls import path
from . import views

urlpatterns = [
    path('insecure/register/', views.insecure_register, name='insecure_register'),
    path('insecure/login/', views.insecure_login, name='insecure_login'),
    path('secure/register/', views.secure_register, name='secure_register'),
    path('secure/login/', views.secure_login, name='secure_login'),
]
