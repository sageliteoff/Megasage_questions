from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from subscriptionpackages.models import SubscriptionPackage

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_package = models.ForeignKey(SubscriptionPackage, on_delete = models.CASCADE,null=True,default=None)
    date_purchased = models.DateTimeField(default=timezone.now)
    total_downloads = models.PositiveIntegerField(default=0)
    downloads_left = models.PositiveIntegerField(default = 0)

    def calc_expiration_date(self):
        # calculate expiration date
        # i.e date of purchases  + duration of subscription_packages
        return (self.date_purchased + timezone.timedelta(days = self.subscription_package.duration))

    def calc_days_left(self):
        #calculate the expiration date
        expiration_date = self.calc_expiration_date()
        #get the date the user subscribe to the package
        date_of_purchase = self.date_purchased
        #calculate the date passed since the puchase of the package
        days_passed = timezone.now() - date_of_purchase
        #calculate the days left for the package to expiration_date (expiration_date - (date_of_purchase + day_passed))
        days_left = (expiration_date - date_of_purchase - days_passed)
        #return 0 if subscription has expire else return the days left
        if (days_left.days <= 0 and days_left.seconds <= 0):
            return 0
        return days_left

    def calc_downloads_left(self):
        #calculte downloads left (downloads available)
        self.downloads_left = max(self.subscription_package.number_of_downloads - self.total_downloads,0)
        self.save()
        if self.downloads_left <= 0:
            return 0
        return self.downloads_left

    def __str__(self):
        return "{0} profile".format(self.user)
