from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.template.loader import render_to_string
import base64
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.contrib.messages import get_messages

import io
from django.db.models import Q
# Create your views here.
def home(request):
    if request.method =='GET':
        user=CustomUser.objects.all()
        return render(request,'home.html',{'user':user})
       
def delete_user(request,id):
    if request.method == 'GET':
       if request.user.is_superuser:
            user=CustomUser.objects.get(id=id).delete()
            user=CustomUser.objects.all()
            context={'user':user}
            messages.success(request, 'user deleted successfully.')
            b=render_to_string('table.html',context,request)

            return JsonResponse( {'b':b} )

def sign_up(request):
    if request.method =='POST':
        if request.user.is_superuser:
            username=request.POST.get('iName')
            first_name=request.POST.get('iFirstName')
            last_name=request.POST.get('iLastName')
            email=request.POST.get('iEmail')
            address=request.POST.get('iAddress')
            mobile=request.POST.get('iMobile')
            imag=request.POST.get('iImage')
            if username and email and mobile:
                user = CustomUser.objects.filter(Q(username=username) | Q(email=email) | Q(mobile=mobile)).first()
                if len(mobile) == 10 and (all(i.isdigit() for i in mobile)):
                    if user is None:              
                        u=CustomUser.objects.all()                  
                        usr = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,address=address,mobile=mobile,password='user@123') 
                        image_data=base64.b64decode(imag)
                        usr.set_password('userk123')
                        m = CustomUser()
                        iimg = ContentFile(image_data,name=f'{username}.jpg')
                        usr.image=iimg

                        usr.save()
                        messages.success(request, 'user created successfully.')
                        context={'user':u}
                        b=render_to_string('table.html',context,request)
                        return JsonResponse( {'k':b})
                    else:
                        messages.error(request, 'user already exist.')       
                else:
                    messages.error(request, 'mobile number is not valid')
            else:
                messages.error(request, 'data required for username,mobile and email')
                u=CustomUser.objects.all()
                django_messages = []
                for message in messages.get_messages(request):
                    django_messages.append({
                    
                        "message": message.message,

                    })
            context={'user':u,'messags':django_messages}
            b=render_to_string('table.html',context,request)
            return JsonResponse( {'k':b})

def sign_in(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        if '@' in username_or_email:
            u=CustomUser.objects.filter(email=username_or_email)
            user = authenticate(username=u.first().username, password=password)
        else:
            user = authenticate(username=username_or_email,password=password)
        if user:
            login(request, user) 
            return redirect("/")
        else:        
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def update_user(request,id):
    if request.method == 'POST':
        username=request.POST.get('iName')
        first_name=request.POST.get('iFirstName')
        last_name=request.POST.get('iLastName')
        email=request.POST.get('iEmail')
        address=request.POST.get('iAddress')
        mobile=request.POST.get('iMobile')
        imag=request.POST.get('iImage')    
        if len(mobile) == 10 and (all(i.isdigit() for i in mobile)):
            u=CustomUser.objects.all()
            if username!=u.first().username or email!=u.first().email or mobile!=u.first().mobile:                
                user=CustomUser.objects.get(id=id)
                user.username=username
                user.email=email
                user.address=address
                user.mobile=mobile
                user.first_name=first_name
                user.last_name=last_name
                if imag:
                    user.image.delete()
                    image_data = base64.b64decode(imag)
                    iimg = ContentFile(image_data,name=f'{username}.jpg')
                    user.image=iimg
                    user.save()
                else:
                    user.save()          

                user1=CustomUser.objects.get(username=username)
            
                notify = Notification.objects.create(user=user1, notify="Profile updated by priciple", read=False)
                notify.save()
                context={'user':u}
                b=render_to_string('table.html',context,request)
  
                return JsonResponse( {'k':b})
            else:
                    messages.error(request, 'user already exist.')       
        else:
            messages.error(request, 'mobile number is not valid')
        u=CustomUser.objects.all()
        django_messages = []
        for message in messages.get_messages(request):
            django_messages.append({
                "message": message.message,
                })
            context={'user':u,'messags':django_messages}
            b=render_to_string('table.html',context,request)
            return JsonResponse( {'k':b})



def notify(request):
    if request.method == 'GET':      
        unread_n=Notification.objects.filter(user=request.user,read=False).values_list('id',flat=True)
        l=list(unread_n)
        read_n=Notification.objects.filter(user=request.user)
        # id_name = [(unread_n.id) for object in unread_n]
        user = CustomUser.objects.filter(username=request.user.username)
        if user:
            d=Notification.objects.filter(user=request.user)
            d.update(read=True)
        return render(request,'notify.html',{'kk':unread_n,'read_n':read_n,'l':l})
      
    
def logout_user(request):
    logout(request)
    return redirect('/sign_in')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def edit(request,id):
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        image=request.FILES.get('image')
        print(username,first_name,last_name,email,address,mobile,image)
        if len(mobile) == 10 or (all(i.isdigit() for i in mobile)):
            u=CustomUser.objects.exclude(username=request.user.username)
            if username!=u.first().username or email!=u.first().email or mobile!=u.first(). mobile:   
                user=CustomUser.objects.filter(id=id)
                user.update(username=username,email=email,first_name=first_name,last_name=last_name,address=address,mobile=mobile,image=image)
                user = CustomUser.objects.get(username=username)
                superuser = CustomUser.objects.get(is_superuser=True)
                notify = Notification.objects.create(user=superuser,notify=f'Profileupdated by {user}', read=False) 
            else:
                messages.error(request, 'user already exist.')
        else:
            messages.error(request, 'mobile number is not valid')

    return render(request,'update.html')