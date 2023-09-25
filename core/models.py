from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import date


class CustomUser(AbstractUser):
    # email = models.EmailField(_('email address'), unique = True)
    address = models.TextField(blank=False)
    mobile = models.IntegerField()
    image = models.ImageField(upload_to='media',blank=True,null=True)

    REQUIRED_FIELDS = ['email','first_name', 'last_name','mobile','address','image']
    def __str__(self):
        return "{}".format(self.email)
    

class Notification(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    notify= models.CharField(max_length=80)
    read = models.BooleanField(default=False) 
    created = models.DateTimeField(auto_now=True)

   



    # def __str__(self):
    #     return self.notify +"    ...........     "+str(self.user)

