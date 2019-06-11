from django.views.generic import TemplateView
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from allauth.account.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from utils.error_messages import errorMessage
from django.utils import timezone

@method_decorator(login_required,name="dispatch")
class ProfilePageView(TemplateView):
    template_name = "userprofile/userprofile.html"
    user_profile = None

    def get(self,*args,**kwargs):
        try:
            self.user_profile = UserProfile.objects.get(user=self.request.user)
            response = super().get(ProfilePageView,args,kwargs)
            
            if not self.user_profile.subscription_package:
                messages.add_message(self.request, messages.ERROR, errorMessage["SPX"])
                return HttpResponseRedirect(redirect_to=reverse("subscription_packages"))

            # check whether the subscription expiration_date has reached
            if self.user_profile.calc_expiration_date() < timezone.now():
                self.user_profile.subscription_package = None
                self.user_profile.save()
            return response
        except  UserProfile.DoesNotExist as e:
            # if current user do not have a userprofile create it for the user
            userprofile = UserProfile(
                user = self.request.user,
                subscription_package = None,)
            userprofile.save()
            return HttpResponseRedirect(redirect_to=reverse("subscription_packages"))

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user_profile:context["userprofile"] = self.user_profile
        return context
