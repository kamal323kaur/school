from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from .resource import *

# Register your models here.

admin.site.register(MyModel)
class CustomUserAdmin(admin.ModelAdmin):  
    list_display = ('id','first_name','last_name','username','email','address')  
    search_fields = ['id','first_name','last_name','username','email','address']

admin.site.register(CustomUser, CustomUserAdmin)

class NotificationAdmin(ImportExportModelAdmin):
     resource_class = NotificationResource  
     readonly_fields=('created',)
admin.site.register(Notification, NotificationAdmin)
