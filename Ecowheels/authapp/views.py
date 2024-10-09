from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import re
import uuid
from .utils import send_email_to_client

def landingpage(request):
    return render(request, 'auth/home.html')

def loginpage(request):
    try:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
                return redirect("login")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Login Successfully")
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
    except Exception as e:
        print(e)
    return render(request, 'auth/login.html')

def signuppage(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "User with the same username already exists.")
                    return redirect("signup")
                user = User.objects.filter(email=email)
                if user.exists():
                    messages.info(request, "Email already exists.")
                    return redirect("signup")
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters long.")
                    return redirect("signup")
                if not re.search(r'[A-Za-z]', password):
                    messages.error(request, "Password must contain at least one letter.")
                    return redirect("signup")
                if not re.search(r'[0-9]', password):
                    messages.error(request, "Password must contain at least one number.")
                    return redirect("signup")
                else:
                    my_user = User.objects.create_user(username, email, password)
                    my_user.save()
                    messages.info(request, "Account created successfully. Please login to continue.")
                return redirect('login')
            except Exception as e:
                print(e)  
    except Exception as e:
        print(e)
    return render(request, 'auth/signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def ForgotPassword(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, "No Username Found with this Username")
                return redirect("forgotpassword")

            # Generate a token and update the user's profile
            token = str(uuid.uuid4())
            profile_obj, created = UserProfile.objects.get_or_create(user=user_obj)
            profile_obj.forgot_password_token = token
            profile_obj.save()

            # Send email to user
            send_email_to_client(user_obj.email, token)
            messages.success(request, "Email has been sent")
            return redirect("forgotpassword")
    except Exception as e:
        print(e)
        messages.error(request, "An error occurred. Please try again.")
    return render(request, "auth/forgotpassword.html")


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = UserProfile.objects.filter(forgot_password_token=token).first()
        if not profile_obj:
            messages.error(request, "Invalid or expired token.")
            return redirect("forgotpassword")

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect(f"/ChangePassword/{token}/")

            if len(new_password) < 8:
                messages.error(request, "Password should be at least 8 characters long.")
                return redirect(f"/ChangePassword/{token}/")
            
            user_obj = profile_obj.user
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, "Password changed successfully. Please log in with your new password.")
            return redirect("login")

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred. Please try again.")
    
    return render(request, "auth/changepassword.html", context)
