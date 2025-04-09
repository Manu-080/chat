from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .tasks import send_welcome_email
from .forms import RegisterForm, LoginForm, UpdateUserForm

User = get_user_model()

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            User.objects.create_user(
                email=email, username=username, password=password, 
                first_name=first_name, last_name=last_name
                )
            
            # CELERY SEND MAIL AFTER USER CREATED ACCOUNT 
            send_welcome_email.delay(email, username)

            return redirect('signin')
        
        else:
            print('user not created !') # for debugging.

    else:
        form = RegisterForm()

    context = {
        'form':form,
    }
    return render(request, 'user/register.html', context)



def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user_auth = authenticate(email=email, password=password)

            if user_auth:
                login(request, user_auth)

                return redirect('dashboard')
            else:
                print('user not logged in') # for debugging
    else:

        form = LoginForm()
    
    context = {
        'form':form,
    }
    return render(request, 'user/signin.html', context)



@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def update_user(request):
    user = request.user # current sign in user

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user) # data = request.POST, instance_object = current user.
        if form.is_valid():
            form.save()

            return redirect('dashboard')
    else:
        form = UpdateUserForm(instance=request.user)

    context = {
        'form':form,
    }
    return render(request, 'user/update_user.html', context)



@login_required(login_url='signin')
def dashboard(request):
    session_id = request.session.session_key # to get current session_key of the current sign in user.
    print(session_id)
    return render(request, 'user/dashboard.html')
