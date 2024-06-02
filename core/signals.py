from django.db.models.signals import post_save,pre_delete,post_delete
from django.dispatch import receiver
from core.models import *
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=CustomUser)
def user_created(sender,instance, created,**kwargs):
   if created:
      user = CustomUser.objects.filter(username=instance.username)
      print("---------------------------------------",user)
      subject = 'welcome to school'
      message = f'Hi {instance.username} you have registered in school and your password is userk123'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [instance.email, ]
      send_mail( subject, message, email_from, recipient_list )


@receiver(pre_delete, sender=CustomUser)
def user_deleted(sender, instance,using=CustomUser, **kwargs):
      user = CustomUser.objects.filter(username=instance.username)
      subject = 'your account is deleted.'
      message = f'Hi {instance.username} your account is deleted.'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [instance.email, ]
      send_mail( subject, message, email_from, recipient_list )


