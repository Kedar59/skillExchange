from django.shortcuts import render, redirect
from .models import *
import re,random,os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
User = get_user_model()
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
from supabase import create_client, Client
url= os.environ.get("SUPABASE_URL")
key= os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
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
def reset_pass(request):
    if request.method == 'POST':
        email = request.POST['email']
        actual_otp = request.POST['actual_otp']
        otp = request.POST['otp']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if otp != actual_otp:
            messages.error(request,"Invalid otp please try again")
            return render(request,"users/get_email.html")
        validity=is_valid_password(password1)
        if validity['valid']!=True:
            messages.error(request,validity['error'])
            return render(request, 'users/get_email.html')
        if password1!=password2:
            messages.error(request,"Passwords dont match please try again")
            return render(request,"users/get_email.html")
        user = User.objects.get(email=email)
        user.set_password(password1)
        user.save()
        
        messages.success(request,"Password reset successfully")
        return render(request,"users/login.html")
        
    return render(request,"users/reset_pass.html")
def get_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,'Invalid email address. Please enter a valid email.')
            return render(request, 'users/get_email.html')
        if not email:
            messages.error(request, 'Email field was empty.')
            return render(request, 'users/get_email.html')
        if not User.objects.filter(email=email).exists():
            messages.error(request,f"User with email {email} dosent have a account on skillExchange")
            return render(request, 'users/get_email.html')
        otp = random.randint(100000,999999)
        subject= f"Email Verification for {email} Account"
        message = "Hello you are recieving this email to reset your password"
        message += "please use the following OTP (One-Time Password):\n\n"
        message += f"OTP: {otp}\n\n"
        message += "This OTP will expire in 15 minutes.\n\n"
        message += "If you didn't try to reset your password please forget it on our website, please ignore this email.\n\n"
        message += "Best regards,\nYour Website Team"
        send_mail(subject,message,EMAIL_HOST_USER,[email],fail_silently=True)
        messages.success(request,f"Email with otp has been sent to : {email}")
        return render(request,'users/reset_pass.html',{'otp':otp,'email':email})
    
    return render(request,"users/get_email.html")
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
            return redirect(profile)  # Redirect to the user's profile page after login
        else:
            messages.error(request, 'Invalid email or password.')
            render(request, 'users/login.html')
    return render(request, 'users/login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')
@login_required
def profile(request):
    user = request.user
    user_skills = user.skills.all()
    all_skills = Skill.objects.all()
    skills_not_possessed = all_skills.difference(user_skills)
    credential_links = {}  # Initialize an empty dictionary

    for skill in user_skills:
        skill_id = skill.id
        credential = Credential.objects.filter(user=user, skill=skill).first()  # Use .first() to get a single credential
        if credential:
            links = credential.links
            credential_links[skill_id] = [{
                'linkName': link.get('linkName'),
                'linkValue': link.get('linkValue')
            } for link in links]
        else:
            credential_links[skill_id] = []  # No credentials for this skill
    print(credential_links)
    context = {
        'user': user,
        'user_skills': user_skills,
        'skills_not_possessed': skills_not_possessed,
        'credential_links': credential_links,
    }
    
    if request.method == 'POST':
        if 'delete_credential' in request.POST:
            link_name = request.POST['link_name']
            skill_id = request.POST['skill_id']
            try:
                # Find the skill and credential associated with the skill and user
                skill = Skill.objects.get(id=skill_id)
                credential = Credential.objects.get(user=user, skill=skill)

                # Retrieve the list of links
                links = credential.links

                # Find the index of the link with the specified link_name
                link_index = None
                for i, link in enumerate(links):
                    if link.get('link_name') == link_name:
                        link_index = i
                        break
                # If the link is found, remove it from the list
                if link_index is not None:
                    del links[link_index]
                    credential.links = links  # Update the links list in the credential
                    credential.save() # Redirect to the user's profile
                    return redirect(profile)
            except (Skill.DoesNotExist, Credential.DoesNotExist):
                # Handle exceptions, e.g., skill or credential not found
                return render(request, 'error.html', {'message': 'Skill or credential not found'})
        elif 'add_credential' in request.POST:
            link_name = request.POST['link_name']
            link = request.POST['link']
            skill_id = request.POST['skill_id']
            skill = Skill.objects.get(id=skill_id)
            credential = Credential.objects.filter(user=user, skill=skill).first()
            if credential:
                # Get the existing links
                links = credential.links
            else:
                # Create a new credential if it doesn't exist
                credential = Credential.objects.create(user=user, skill=skill)
                links = []

            # Create a new JSON object
            new_link = {
                'linkName': link_name,
                'linkValue': link,
            }

            # Append the new link to the list
            links.append(new_link)

            # Update the credential's links
            credential.links = links
            credential.save()
            return redirect(profile)
        elif 'update_first_name' in request.POST:
            new_first_name = request.POST['update_first_name']
            user.first_name = new_first_name
            user.save()

            if user.first_name != new_first_name:
                messages.error(request, 'An error occurred while updating the first name. Please try again')
                return render(request, "users/profile.html" , context)
            
            messages.success(request, ' First name updated successfully ')
            return render(request, "users/profile.html" , context)
        elif 'update_last_name' in request.POST:
            new_last_name = request.POST['update_last_name']
            user.last_name = new_last_name
            user.save()

            if user.last_name != new_last_name:
                messages.error(request, 'An error occurred while updating the last name. Please try again')
                return render(request, "users/profile.html" , context)
            
            messages.success(request, ' Last name updated successfully ')
            return render(request, "users/profile.html" , context)
        elif 'delete_skills_to_user' in request.POST:
            delete_skill_ids = request.POST.getlist("delete_skills")
            skills_to_delete = Skill.objects.filter(id__in=delete_skill_ids)
            user.skills.remove(*skills_to_delete)
            user.save()
            return redirect(profile)
        elif 'add_skills_to_user' in request.POST:
            selected_skill_ids = request.POST.getlist("selected_skills")
            selected_skills = Skill.objects.filter(id__in=selected_skill_ids)
            user.skills.add(*selected_skills)
            user.save()
            return redirect(profile)
        elif 'update_userBio' in request.POST:
            new_userBio = request.POST['update_userBio']
            user.userBio = new_userBio
            user.save()

            if user.userBio != new_userBio:
                messages.error(request, 'An error occurred while updating the user Bio. Please try again')
                return render(request, "users/profile.html" , context)
            
            messages.success(request, ' User Bio updated successfully ')
            return render(request, "users/profile.html" , context)
        elif 'reset_password' in request.POST:
            otp = random.randint(100000,999999)
            subject= f"Email Verification for {user.email} Account"
            message = "Hello you are recieving this email to reset your password"
            message += "please use the following OTP (One-Time Password):\n\n"
            message += f"OTP: {otp}\n\n"
            message += "This OTP will expire in 15 minutes.\n\n"
            message += "If you didn't try to reset your password please forget it on our website, please ignore this email.\n\n"
            message += "Best regards,\nYour Website Team"
            send_mail(subject,message,EMAIL_HOST_USER,[user.email],fail_silently=True)
            messages.success(request,f"Email with otp has been sent to : {user.email}")
            return render(request,'users/reset_pass.html',{'otp':otp,'email':user.email})
        elif 'delete_prof_pic' in request.POST:
            old_file_name: str = f"{user.username}.{user.prof_extension}"
            storage_bucket: str = 'profile_picture'
            response = supabase.storage.from_(storage_bucket).remove(old_file_name)
            user.prof_path = None
            user.prof_extension = None
            user.has_prof_pic = False    
            user = user.save()
            return redirect(profile)
        elif 'update_prof_pic' in request.FILES:
            prof_pic = request.FILES['update_prof_pic']
            if prof_pic.size > 250 * 1024:
                messages.error(request,"Your profie picture is more than 250kb try again")
                return render(request,'users/profile.html',context)
            extension: str = prof_pic.name.split('.')[-1].lower()

            # Define the storage bucket name (replace with your actual bucket name)
            storage_bucket: str = 'profile_picture'
            file_name: str = f"{user.username}.{extension}"
            if request.user.has_prof_pic:
                # delete the file from "profile_picture" bucket in supabase bucket with
                old_file_name: str = f"{user.username}.{user.prof_extension}"
                response = supabase.storage.from_(storage_bucket).remove(old_file_name)
            
            response = supabase.storage.from_(storage_bucket).upload(
                file_name,
                prof_pic.read(),
                {"content-type":f"image/{extension}"}
            )

            if response.status_code != 200:
                messages.error(request, f"{response.status_code}Something went wrong while saving profile picture")
                return render(request,'users/profile.html',context)
            public_url: str = supabase.storage.from_(storage_bucket).get_public_url(file_name)
            user.prof_path = public_url
            user.prof_extension = extension
            user.has_prof_pic = True    
            user = user.save()    
            if user is None:
                messages.error(request,"some error occoured while saving public url")
                return render(request,'users/profile.html',context)
            messages.success(request, "profile picture updated successfully")
            return render(request,'users/profile.html',context)
            
    return render(request, "users/profile.html",context)