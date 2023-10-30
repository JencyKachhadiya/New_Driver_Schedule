from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse

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
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                CurrentUser_ = request.user
                if CurrentUser_.groups.filter(name='Driver').exists():
                    request.session['user_type'] = 'Driver'
                    return redirect('index')
                    
                elif CurrentUser_.groups.filter(name='Accounts').exists():
                    request.session['user_type'] = 'Accounts'
                    return redirect('Account:index')
                else:
                    request.session['user_type'] = 'SuperUser'
                    return redirect('Account:index')
            else:
                messages.error(request, "Login failed!")
                return redirect(request.META.get('HTTP_REFERER'))
                return redirect('login')
    

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

def changePasswordView(request):
    return render(request, 'change-password.html')

@csrf_protect
@api_view(['POST'])
def changePasswordChange(request):
    oldPassword = request.POST.get('oldPassword')
    newPassword = request.POST.get('newPassword')
    reEnterPassword = request.POST.get('reEnterNewPassword')
    
    if newPassword != reEnterPassword:
        messages.error(request, "Both new password must be same.")
        return redirect(request.META.get('HTTP_REFERER')) 
    if request.user.is_authenticated:
        user_email = request.user.email
        print(user_email)
        return HttpResponse(user_email)
        userData = User.objects.filter(username=logInUser.username).first()
        
        stored_password = user.password  # Get the hashed password from the User model
        is_password_match = check_password(provided_password, stored_password)
    else:
        return HttpResponse('user not login')