import random
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import connection
from .models import User

# Helper function for email validation
def validate_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
        return True
    except ValidationError:
        return False

# Helper function to generate a random OTP
def generate_otp():
    return random.randint(100000, 999999)

def register(request):
    try:
        if request.method == 'POST':
            # Collect form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Validation checks
            errors = []
            if len(first_name) > 25:
                errors.append('First name cannot exceed 25 characters.')
            if len(last_name) > 25:
                errors.append('Last name cannot exceed 25 characters.')
            if len(password) < 8:
                errors.append('Password must be at least 8 characters long.')
            if not validate_email(email):
                errors.append('Please enter a valid email address.')

            # If there are validation errors, show messages and return to form
            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'register.html')

            # Generate OTP and store it in the session
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['registration_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
            }

            # Send OTP to the user's email
            send_mail(
                'Your OTP for Verification',
                f'Your OTP is: {otp}',
                'integerdatatype@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.info(request, f"OTP sent to {email}. Please check your email.")
            return redirect('verify_otp')  # Redirect to OTP verification page

        return render(request, 'register.html')

    finally:
        connection.close()  # Ensure database connection is closed after each request

def verify_otp(request):
    try:
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')

            # Get the OTP stored in the session
            stored_otp = request.session.get('otp')
            registration_data = request.session.get('registration_data')

            if entered_otp and stored_otp and int(entered_otp) == int(stored_otp):
                # OTP is correct, now save the user to the database
                hashed_password = make_password(registration_data['password'])
                new_user = User.objects.create(
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    password=hashed_password
                )

                # Clear the session data
                del request.session['otp']
                del request.session['registration_data']

                messages.success(request, 'Email verified successfully! You can now log in.')
                return redirect('login')  # Redirect to login page after successful verification
            else:
                messages.error(request, 'Invalid OTP. Please try again.')

        return render(request, 'verify.html')

    finally:
        connection.close()  # Ensure database connection is closed after each request


def login(request):
    return render(request, 'login.html')
