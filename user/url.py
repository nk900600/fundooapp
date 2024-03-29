from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import include, url


# all the urls are called
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.Registrations.as_view(), name="registration"),

    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.Login.as_view(), name="login"),
    path('forgotpassword', views.ForgotPassword.as_view(),name="forgotPassword"),
    path('activate/<surl>/', views.activate, name="activate"),
    path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    path('resetpassword/<user_reset>', views.ResetPassword.as_view(), name="resetpassword"),
    path('logout/', views.Logout.as_view() ,name="logout"),
    path('session/', views.session),
    # path('hello/', views.Hello.as_view(), name ="hello"),


]