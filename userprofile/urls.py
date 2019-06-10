from django.urls import path, include
from .views import ProfilePageView

urlpatterns = [
    path("",ProfilePageView.as_view(), name="user_profile")
]
