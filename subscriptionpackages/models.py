from django.db import models
from django.utils import timezone
class SubscriptionPackage(models.Model):
    NAME_CHOICES = [
        ("Free","Free"),
        ("Small","Small"),
        ("Standard","Standard"),
        ("Ultimate","Ultimate")]
    #The name of the package (must be a name from the NAME_CHOICES list)
    name = models.CharField(max_length=100,unique=True,choices = NAME_CHOICES)
    #Days it takes before subscribe package expires
    duration = models.IntegerField(default=1)
    #The date the subscription was added to database
    date_introduced = models.DateTimeField(default=timezone.now)
    #A brief description of the Package
    description = models.TextField(blank=True)
    #The number of download the package gives to a user
    number_of_downloads = models.PositiveIntegerField(default = 4)
    #The price of the Package
    price = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return "{0} {1} days package".format( self.name,self.duration,)
