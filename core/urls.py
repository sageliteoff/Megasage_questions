from django.contrib import admin
from django.urls import path,include,re_path
import allauth,home,subscriptionpackages,userprofile
from filebrowser.sites import site

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("accounts/",include("allauth.urls")),
    path("subscriptionpackages/",include("subscriptionpackages.urls")),
    path("userprofile/",include("userprofile.urls")),
    re_path(r'^tinymce/', include('tinymce.urls')),
     path('admin/filebrowser/', site.urls),
]
