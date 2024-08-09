from django.urls import path
from . import views

urlpatterns = [
    path('insecure/register/', views.insecure_register, name='insecure_register'),
    path('insecure/login/', views.insecure_login, name='insecure_login'),
    path('secure/register/', views.secure_register, name='secure_register'),
    path('secure/login/', views.secure_login, name='secure_login'),
    path('secure/2fa/setup/', views.setup_2fa, name='setup_2fa'),  # Add 2FA setup URL
    path('secure/2fa/verify/', views.verify_2fa, name='verify_2fa'),  # Add 2FA verification URL
]
