from core.models import *
def notify(request):
        try:
            unread_n=Notification.objects.filter(user=request.user,read=False)   
            read_n=Notification.objects.filter(user=request.user,read=True)
            c=unread_n.count()     
            return {'n_c':c,'not_read':unread_n}
        except:
            return {}
       