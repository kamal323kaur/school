from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name="home"),
    path('sign_in/',sign_in,name="sign_in"),
    path('sign_up/',sign_up,name="sign_up"),
    path('update_user/<int:id>',update_user,name="update_user"),
    path('edit/<int:id>',edit,name="edit"),
    path('change_password/',change_password,name="change_password"),
    path('notify/',notify,name="notify"),
    path('logout/',logout_user,name="logout"),
    
    path('delete_user/<int:id>',delete_user,name="delete_user"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

