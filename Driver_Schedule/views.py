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
import logging
from django.http import HttpResponseServerError

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()     

def index(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        logger.exception(f"An exception occurred in the index view: {e}")
        return HttpResponseServerError("An error occurred")

def loginCall(request):
    try:
        return render(request, 'login.html')
    except Exception as e:
        logger.exception(f"An exception occurred in the loginCall view: {e}")
        return HttpResponseServerError("An error occurred")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

@csrf_protect
def loginCheck(request):
    try:
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
                try:
                    driverObj = Driver.objects.filter(Q(Q(name=username) | Q(email=username) | Q(driverId=driverId)) & Q(password=password)).first()
                    userObj = User.objects.filter(Q(username=username) | Q(email=username)).first()
                except Exception as e:
                    logger.exception(f"Error querying Driver and User objects: {e}")
                    return HttpResponseServerError("An error occurred while querying user data")
                
                if userObj or driverObj:
                    try:
                        username = driverObj.name if driverObj else userObj.username
                        user = authenticate(
                            username=username,
                            password=password,
                        )
                    except Exception as e:
                        logger.exception(f"Error authenticating user: {e}")
                        return HttpResponseServerError("An error occurred while authenticating user")

                    if user:
                        try:
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
                        except Exception as e:
                            logger.exception(f"Error during login process: {e}")
                            return HttpResponseServerError("An error occurred during login process")
                    else:
                        messages.error(request, "Authentication failed!")
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, "User not found!")
                    return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        logger.exception(f"An exception occurred in the loginCheck view: {e}")
        return HttpResponseServerError("An error occurred")
  
def CustomLogOut(request):
    try:
        logout(request)
        messages.success(request, "Logout successfully")
        return redirect('login')
    except Exception as e:
        logger.exception(f"An exception occurred in the CustomLogOut view: {e}")
        return HttpResponseServerError("An error occurred during logout")


    # Check if the user is a member of the "driver" group
    is_driver = user.groups.filter(name='driver').exists()

    context = {
        'is_driver': is_driver,
    }

    return render(request, 'your_template.html', context)

def CustomForgetPassword(request):
    try:
        return render(request , 'forgetPassword.html')
    except Exception as e:
        logger.exception(f"An exception occurred in the CustomForgetPassword view: {e}")
        return HttpResponseServerError("An error occurred")

@csrf_protect
@api_view(['POST'])
def ForgetMail(request):
    try:
        driverEmail = request.POST['email']

        try:
            userObj = User.objects.filter(email=driverEmail).first()
            driverObj = Driver.objects.filter(email=userObj.email).first()
        except Exception as e:
            logger.exception(f"Error querying User and Driver objects: {e}")
            return HttpResponseServerError("An error occurred while querying user and driver data")

        if userObj and driverObj:
            try:
                subject = 'Forget Password Request'
                message = f'Your old password is {driverObj.password}'
                from_email = 'your@email.com'
                send_mail(subject, message, from_email, [driverEmail])
                logger.info(f"Password reset email sent successfully to {driverEmail}")
                messages.success(request, "Password reset email sent successfully.")
            except Exception as e:
                logger.exception(f"Error sending password reset email: {e}")
                messages.error(request, "An error occurred while sending the password reset email.")
        else:
            logger.warning(f"Invalid email address: {driverEmail}")
            messages.error(request, "This email is not valid!")

    except Exception as e:
        logger.exception(f"An exception occurred in the ForgetMail view: {e}")
        messages.error(request, "An error occurred while processing your request.")

    return redirect(request.META.get('HTTP_REFERER'))

def changePasswordView(request):
    try:
        return render(request, 'change-password.html')
    except Exception as e:
        logger.exception(f"An exception occurred in the changePasswordView function: {e}")
        return HttpResponseServerError("An error occurred while processing your request.")

@csrf_protect
def changePasswordChange(request):
    try:
        if request.user.is_authenticated:
            oldPassword = request.POST.get('oldPassword')
            newPassword = request.POST.get('newPassword')
            reEnterPassword = request.POST.get('reEnterNewPassword')

            curUser = request.user
            stored_password = curUser.password
            try:
                if check_password(oldPassword, stored_password):
                    try:
                        if newPassword != reEnterPassword:
                            messages.error(request, "Both new password must be same.")
                            return redirect(request.META.get('HTTP_REFERER'))
                        else:
                            curUser.set_password(newPassword)
                            curUser.save()
                            if curUser.groups.filter(name='Driver').exists():
                                driver = Driver.objects.get(email=curUser.email)
                                driver.password = newPassword
                                driver.save()

                            messages.success(request, "Password changed, Please logIn again.")
                            return redirect('login')
                    except Exception as e:
                        logger.exception(f"Error changing password for user: {e}")
                        return HttpResponseServerError("An error occurred while changing password")
                else:
                    messages.error(request, "Your old password is incorrect.")
                    return redirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                logger.exception(f"Error checking old password: {e}")
                return HttpResponseServerError("An error occurred while checking old password")
        else:
            messages.error(request, "User not logged In.")
            return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        logger.exception(f"An exception occurred in the changePasswordChange function: {e}")
        return HttpResponseServerError("An error occurred while processing your request.")    
    
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
                userData['driverId'] = driverObj.driverId
                
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

