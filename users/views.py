from django.shortcuts import render, redirect
from .models import *
import re,random,os
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



# for email verification
from django.core.mail import send_mail
from skillExchange.settings import EMAIL_HOST_USER
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def verifyOTP(request):
    if request.method=='POST':
        username=request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        userBio = request.POST['userBio']
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        userBio=userBio
                                        )
        if user is not None:
            messages.success(request,'Tanks for confirming your email registration successful')
            return redirect(login_view)
        else:
            messages.error(request,'There was some issue plz try again')
            return redirect(register)
    return JsonResponse({'data':'data'},status=200)
# from .forms import RegistrationForm
# import os
# from supabase import create_client, Client
# url= os.environ.get("SUPABASE_URL")
# key= os.environ.get("SUPABASE_KEY")
# supabase = create_client(url, key)
# Create your views here.

def is_valid_password(password):
    pattern = r"^(?=.*[@#$%^&+=])(?=\S+$)"
    validity={'valid':True,'error':"No error found"}
    if not len(password)>=8:
        validity['valid']=False
        validity['error']="Password must be at least 8 characters long"
        return validity
    if re.match(pattern, password):
        return validity
    else:
        validity['valid']=False
        validity['error']="Must contain a special character like @,#,$,%,^,&,+ or = and must not contain spaces."
        return validity
def home(request):
    return render(request, "users/home.html")

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        userBio = request.POST['userBio']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,'Invalid email address. Please enter a valid email.')
            return render(request, 'users/register.html')
        if not (username and email and password1 and password2 and first_name and last_name and userBio):
            messages.error(request, 'All fields are required.')
            return render(request, 'users/register.html')
        validity=is_valid_password(password1)
        if validity['valid']!=True:
            messages.error(request,validity['error'])
            return render(request, 'users/register.html')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'users/register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already registered.')
            return render(request, 'users/register.html')  
        otp = random.randint(100000,999999)
        subject= f"Email Verification for {email} Account"
        message = f"Hi {username},\n\n"
        message += "Thank you for registering on our website. To verify your email address and activate your account, "
        message += "please use the following OTP (One-Time Password):\n\n"
        message += f"OTP: {otp}\n\n"
        message += "This OTP will expire in 15 minutes.\n\n"
        message += "If you didn't register on our website, please ignore this email.\n\n"
        message += "Best regards,\nYour Website Team"
        send_mail(subject,message,EMAIL_HOST_USER,[email],fail_silently=True)
        messages.success(request,f"Email with otp of account {username} to email: {email}")
        return render(request,'users/verify.html',{'otp':otp,'username':username,'first_name':first_name,'last_name':last_name,'password':password1,'email':email,'userBio':userBio})
        
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if not email:
            messages.error(request, 'Email field was empty.')
            return render(request, 'users/login.html')
        if not password:
            messages.error(request, 'Password field was empty.')
            return render(request, 'users/login.html')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # User authentication successful, log them in
            login(request, user)
            return redirect(home)  # Redirect to the user's profile page after login
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'users/login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')
@login_required
def profile(request):
    user = request.user
    return render(request, "users/profile.html",{'user':user})