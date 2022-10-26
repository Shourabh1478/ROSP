from re import U
from django.contrib import auth
from django.core.checks import messages
from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from .forms import CreateUserForm
from store.models import Customer
from django.db import models
import secrets
from django.db.models.signals import post_save
import uuid
from .models import *
from store.models import *
from store.utils import cartData




# data= User.objects.all()
# # user= list(data)
# # for i in user:
# #     print(i)
# data= Profile.objects.all()
# profile= list(data)
# for i in profile:
#     print(i.user)

# print(referral)


# class UniqueCodes(models.Model):
#     """
#     Class to create human friendly gift/coupon codes.
#     """

#     # Model field for our unique code
#     code = models.CharField(max_length=8, blank=True, null=True, unique=True)

#     @classmethod
#     def post_create(cls, sender, instance, created, *args, **kwargs):
#         """
#         Connected to the post_save signal of the UniqueCodes model. This is used to set the
#         code once we have created the db instance and have access to the primary key (ID Field)
#         """
#         # If new database record
#         if created:
#             # We have the primary key (ID Field) now so let's grab it
#             id_string = str(instance.id)
#             # Define our random string alphabet (notice I've omitted I,O,etc. as they can be confused for other characters)
#             upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
#             # Create an 8 char random string from our alphabet
#             random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
#             # Append the ID to the end of the random string
#             instance.code = (random_str + id_string)[-8:]
#             # Save the class instance
#             instance.save()

#     def __str__(self):
#         return "%s" % (self.code,)

# Gift= UniqueCodes()
# # Connect the post_create function to the UniqueCodes post_save signal
# post_save.connect(Gift.post_create, sender=UniqueCodes)



def Signup_view(request):
    if 'email_signup' in request.POST:
        username = request.POST['username_signup']
        email = request.POST['email_signup']
        pass1 = request.POST['psw_signup1']
        pass2 = request.POST['psw_signup2']
        code= request.POST['referral']


        if pass1 != pass2:
            return render(request,'Login.html')
        profile= Profile.objects.all()
        d= dict()
        l1= list(profile)
        for i in l1:
            d[i.referral_code]= i.user
        print(d)
        print(code)
        if code:
            for i in d:
                if code==i:
                    profile1= Profile.objects.get(referral_code=code)
                    profile1.count1= profile1.count1+1
                    profile1.save()


        data= User.objects.all()
        user= list(data)
        l=list()
        for i in user:
            l.append(i)
        
            
        referral= ""
        if username not in l:
            referral= uuid.uuid4()

        myuser = User.objects.create_user(username=username,email=email,password = pass1)
        myuser.save()
        print("bbhjscbjbjcsj")
        custuser = Customer.objects.create(user=myuser,name=username,email=email)
        custuser.save()
        profile= Profile.objects.create(user=myuser,referral_code= referral)
        profile.save()

        return redirect('/')

    elif 'email' in request.POST:
        loginusername = request.POST['email']
        loginpassword = request.POST['psw']

        user = authenticate(username = loginusername,password = loginpassword)
        
        if user is not None:
            print('inside')
            login(request,user)
            print('successful')
            return redirect('store')
        else:
            print('failed')
            return redirect('/')

    return render(request,'Login.html')

def Landing_page(request):
    return render(request,'Landing.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')

def Coupons_view(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # context = {'cartItems':cartItems}

    user= request.user
    print(user)
    profile= Profile.objects.all()
    print(profile)
    for i in profile:
        if i.user==user:
            code=i.referral_code
            count2= i.count1

    context = {'cartItems':cartItems,'referral':code,'count':range(count2)}



    return render(request,'store/coupons.html',context)