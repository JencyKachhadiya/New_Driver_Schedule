from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User , Group
from GearBox_app.models import *
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from CRUD import *

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
     return user.groups.filter(name=group_name).exists()     

def index(request):
    return render(request,'index.html')

def loginCall(request):
    return render(request,'login.html') 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

@csrf_protect   
def loginCheck(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            driverId = int(username)
        except:
            driverId = None

        if form.is_valid():            
            driverObj = Driver.objects.filter(Q(Q(name=username) | Q(email=username) | Q(driverId=driverId)) & Q(password=password)).first()
            userObj = User.objects.filter(Q(username=username) | Q(email=username)).first()
            
            if userObj or driverObj:
                username = driverObj.name if driverObj else userObj.username
                user = authenticate(
                    username=username,
                    password=password,
                )                
                if user:
                    login(request, user)
                    CurrentUser_ = request.user
                    if CurrentUser_.groups.filter(name='Driver').exists():
                        request.session['user_type'] = 'Driver'
                        messages.success(request, f"Hi, {CurrentUser_.username}!")
                        return redirect('index')
                    elif CurrentUser_.groups.filter(name='Accounts').exists():
                        request.session['user_type'] = 'Accounts'
                        return redirect('Account:index')
                    elif CurrentUser_.groups.filter(name='HR').exists():
                        request.session['user_type'] = 'HR'
                        return redirect('Account:index')
                    else:
                        request.session['user_type'] = 'SuperUser'
                        return redirect('Account:index')
                else:
                    messages.error(request, "Authentication failed!")
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "User not found!")
                return redirect(request.META.get('HTTP_REFERER'))    

def CustomLogOut(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('login')


    # Check if the user is a member of the "driver" group
    is_driver = user.groups.filter(name='driver').exists()

    context = {
        'is_driver': is_driver,
    }

    return render(request, 'your_template.html', context)

def CustomForgetPassword(request):
    return render(request , 'forgetPassword.html')

@csrf_protect
@api_view(['POST'])
def ForgetMail(request):
    driverEmail = request.POST['email']
    try:
        
        userObj = User.objects.filter(email=driverEmail).first()
        driverObj = Driver.objects.filter(email = userObj.email).first()
        subject = 'Forget Password  Request'
        message = f'Your old password is  {driverObj.password} '
        from_email = 'your@email.com'  # Replace with your email

        # Send the email
        send_mail(subject, message, from_email, [driverEmail])
        messages.success(request, "Password reset email sent successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    
    except:
        messages.error(request, "This email is not valid !")
        return redirect(request.META.get('HTTP_REFERER'))

def changePasswordView(request):
    return render(request, 'change-password.html')

@csrf_protect
def changePasswordChange(request):
    if request.user.is_authenticated:
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        reEnterPassword = request.POST.get('reEnterNewPassword')
         
        curUser = request.user
        stored_password = curUser.password  # Get the hashed password from the User model

        if check_password(oldPassword, stored_password):
            if newPassword != reEnterPassword:
                messages.error(request, "Both new password must be same.")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                curUser.set_password(newPassword)
                curUser.save()

                if curUser.groups.filter(name='Driver').exists():
                    driver = Driver.objects.get(email = curUser.email)
                    driver.password = newPassword
                    driver.save()
                    
                messages.success(request, "Password changed, Please logIn again.")
                return redirect('login')
        else:
            messages.error(request, "Your old password is incorrect.")
            return redirect(request.META.get('HTTP_REFERER'))  
        
    else:
        messages.error(request, "User not logged In.")
        return redirect(request.META.get('HTTP_REFERER')) 
    
    
    
    
# --------------------------------------------------------------------------------------------------------------------------------
# API functions
# --------------------------------------------------------------------------------------------------------------------------------

@csrf_protect
@api_view(['POST'])
def apiLoginCheck(request):
    username = request.POST.get('username').strip()
    password = request.POST.get('password').strip()
    if username and password:
        try:
            driverId = int(username)
        except:
            driverId = None

        driverObj = Driver.objects.filter(Q(Q(name=username) | Q(email=username) | Q(driverId=driverId)) & Q(password=password)).first()
        
        if driverObj:
            user = authenticate(username=driverObj.name, password=password)
            if user:
                userData = User.objects.filter(username=str(user)).values('id','username','first_name','last_name','email').first()
                userData['user_type'] = 'Driver'
                shiftObj = DriverShift.objects.filter(driverId=Driver.objects.filter(name=userData['username']).first().driverId, endDateTime=None).first()
                if shiftObj:
                    tripObj = DriverShiftTrip.objects.filter(shiftId=shiftObj.id, endDateTime=None).first()
                    userData['currentShiftId'] = shiftObj.id if shiftObj else None
                    userData['currentTripId'] = tripObj.id if tripObj else None
                
                return JsonResponse({'status':True,
                                     'message': 'Data fetching successfully.',
                                     'data':userData})
            else:
                return JsonResponse({'status':False, 'message':'Incorrect password.'})
        else:
            return JsonResponse({'status':False, 'message':'User not found.'})
    else:
        return JsonResponse({'status':False, 'message': ('username' if not username else 'password') + ' not found.'})

