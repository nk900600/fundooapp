"""fundoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .swagger_view import schema_view
from rest_framework_simplejwt import views as jwt_views

from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include('user.url')),
    path("social/",include('socialapp.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("api/",include('note.url')),
    url('fundoo/',schema_view, name="swagger"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^accounts/', include('allauth.urls')),
]
