from home.models import College

def programmes(request):
    #return all the objects in the College table 
    return {"colleges":College.objects.all()}
