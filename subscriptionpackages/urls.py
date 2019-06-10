from django.urls import path
from .views import(SubscriptionPackagesView,PurchaseSubscriptionPackagesView)

urlpatterns = [
    path('', SubscriptionPackagesView.as_view(),name="subscription_packages"),
    path('purchase/<int:id>', PurchaseSubscriptionPackagesView.as_view(),name="purchase_subscription_package"),
]
