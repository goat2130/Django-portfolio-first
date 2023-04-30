from django.contrib import admin
from django.urls import path, include
from myapp.views import post_list

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
]
