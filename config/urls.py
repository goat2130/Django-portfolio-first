from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView
from myapp.views import SignUpView, profile, increment_views, ranking, my_posts, follow, unfollow, followers,delete_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('myapp.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<str:username>/', profile, name='profile'),
    path('post/<slug:slug>/increment_views/', increment_views, name='increment_views'),
    path('ranking/', ranking, name='ranking'),
    path('my_posts/', my_posts, name='my_posts'),
    path('follow/<str:username>/', follow, name='follow'),
    path('unfollow/<str:username>/', unfollow, name='unfollow'),
    path('followers/<str:username>/', followers, name='followers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
