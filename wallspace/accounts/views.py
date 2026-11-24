from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)

            if not remember:
                request.session.set_expiry(0)

            return redirect('login_page')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')

        if not all([full_name, email, password, confirm_password]):
            messages.error(request, 'Please complete all fields.')

        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Email address is already registered.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif not terms:
            messages.error(request, 'Please agree to the Terms of Service.')

        else:
            try:
                validate_password(password)

                User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=full_name,
                    password=password
                )

                messages.success(request, 'Account created successfully.')
                return redirect('login_page')

            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)

    return render(request, 'accounts/register.html')