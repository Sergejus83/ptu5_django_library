from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.validators import validate_email

User = get_user_model()
# Create your views here.
@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        error = False

        if not username or User.objects.filter(username=username).first():
            messages.error(request, 'Username not entered or already exists')
            error = True

        if not email or User.objects.filter(email=email).first():
            messages.error(request, 'Email not entered or this email already exists')
            error = True
        else:
            try:
                validate_email(email)
            except:
                messages.error(request, 'Invalid email')
        if not password or not password2 or password != password2:
            messages.error(request, 'Password not entered or not the same')
            error = True

        if not error:
            # sukuriam useri
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'User {username} registration successfull. You can log in now')
            return redirect('login')

    return render(request, 'user_profile/register.html')

@login_required
def profile(request):
    return render(request, 'user_profile/profile.html')