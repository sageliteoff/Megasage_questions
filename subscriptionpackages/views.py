from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .models import SubscriptionPackage
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from allauth.account.decorators import login_required
from userprofile.models import UserProfile
from .forms import PaymentForm
from requests.auth import HTTPBasicAuth
import requests
import json

@method_decorator(login_required, name="dispatch")
class SubscriptionPackagesView(TemplateView):
    template_name = "subscriptionpackages/packages_page.html"
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["free_package"] = SubscriptionPackage.objects.get(name="Free")
        context["small_package"] = SubscriptionPackage.objects.get(name="Small")
        return context

@method_decorator(login_required, name="dispatch")
class PurchaseSubscriptionPackagesView(View):
    package,userprofile = None,None
    def get(self,*args,**kwargs):
        paymentForm = PaymentForm()
        try:
            #get the subscription_package selected by the user and his UserProfile
            package = SubscriptionPackage.objects.get(id=kwargs["id"])
            userprofile = UserProfile.objects.get(user=self.request.user)

            #warn user when he tries to buy a new package but already has some downloads left
            if userprofile.subscription_package and userprofile.calc_downloads_left() > 0:
                return HttpResponse("You Already have a {} package".format(userprofile.subscription_package))

        except SubscriptionPackage.DoesNotExist as e:
            return HttpResponse("<h1>This Package Currently does not exist. choose a different package")
        if package ==  SubscriptionPackage.objects.get(name="Free"):
            return render(
                self.request,
                template_name="subscriptionpackages/payment.html",
                context={"package":package})
        return render(
            self.request,
            template_name="subscriptionpackages/payment.html",
            context={"package":package, "payment_form":paymentForm})

    def post(self,*args,**kwargs):
        package =  SubscriptionPackage.objects.get(id=kwargs["id"])
        userprofile = UserProfile.objects.get(user=self.request.user)
        print(package,userprofile)
        if package.name.lower() == "free":
            messages.add_message(self.request, messages.SUCCESS, ' subscription is succcesful')
            userprofile.subscription_package = package
            userprofile.total_downloads = 0
            userprofile.downloads_left =  package.number_of_downloads
            userprofile.save()

        else:
            paymentForm = PaymentForm(self.request.POST)
            if paymentForm.is_valid():
                vendor = self.request.POST["vendor"]
                billing_number = paymentForm.cleaned_data["mobileNumberInput"]
                billing_reference = paymentForm.cleaned_data["referenceInput"]
                vodafone_token = paymentForm.cleaned_data["vodafoneTokenInput"]
                print(billing_number)
                api_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{MerchantAccountNumber}/receive/mobilemoney"
                api_url = "https://google.com"
                headers = {
                    'Content-Type': "application/json",
                    'Cache-Control': "no-cache",
                    'megasage-Token': "513c06fe-e788-4dfb-9089-3f834be928bb"
                    }
                data = {
                      "CustomerName": "Customer FullName",
                      "CustomerMsisdn": "054XXXX",
                      "CustomerEmail": "",
                      "Channel": "mtn-gh",
                      "Amount": 0.8,
                      "PrimaryCallbackUrl": "http://requestb.in/1minotz1",
                      "SecondaryCallbackUrl": "http://requestb.in/1minotz1",
                      "Description": "T Shirt",
                      "ClientReference": "",
                      "Token": "string"
                    }
                            #if payment is successful add it the update the Userprofile subscription_package
                payload = json.dumps(data)

                #response = requests.post(url=api_url,auth = HTTPBasicAuth("kpsxolou","ixahwlao"),data = payload)

            is_payment_successful = False
            if is_payment_successful:
                messages.add_message(self.request, messages.SUCCESS, ' payment is succcesful')
                self.userprofile.subscription_package = self.package
                self.userprofile.total_downloads = 0
                self.userprofile.downloads_left =  self.package.number_of_downloads
                self.userprofile.save()
            else:
                # payment is not succcesful
                messages.add_message(self.request, messages.ERROR, 'payment failed.')

        return HttpResponseRedirect(redirect_to=reverse("user_profile"))
