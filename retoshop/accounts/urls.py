from django.urls import path
from .views import login, register, verify_otp

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/', verify_otp, name='verify_otp'),
    path('login/', login, name='login'),  # Assuming you have a login view
    # Add other URL patterns here
]
