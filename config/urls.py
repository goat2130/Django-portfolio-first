from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView
from myapp.views import SignUpView, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('myapp.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
]
