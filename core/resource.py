from import_export import resources 
from .models import *
class NotificationResource(resources.ModelResource):
     class Meta:
         model = Notification
