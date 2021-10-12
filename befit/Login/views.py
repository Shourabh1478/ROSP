from django.core.checks import messages
from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from .forms import CreateUserForm


def Signup_view(request):
    if 'email_signup' in request.POST:
        username = request.POST['username_signup']
        email = request.POST['email_signup']
        pass1 = request.POST['psw_signup1']
        pass2 = request.POST['psw_signup2']

        if pass1 != pass2:
            return render(request,'Login.html')

        myuser = User.objects.create_user(username=username,email=email,password = pass1)
        myuser.save()
        return redirect('/')

    elif 'email' in request.POST:
        loginusername = request.POST['email']
        loginpassword = request.POST['psw']

        user = authenticate(username = loginusername,password = loginpassword)
        
        if user is not None:
            print('inside')
            login(request,user)
            print('successful')
            return redirect('/')
        else:
            print('failed')
            return redirect('/')

    return render(request,'Login.html')

def Landing_page(request):
    return render(request,'Landing.html')