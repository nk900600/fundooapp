from django.urls import path
from . import views
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from django.conf.urls import include, url
from fundooapp.swagger_view import schema_view



# all the urls are called
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.Registrations.as_view()),
    path('auth/jwt/', obtain_jwt_token),
    path('auth/jwt/refresh', refresh_jwt_token),
    path('login/', views.Login.as_view()),
    path('login/forgotpassword', views.forgot_password),
    path('activate/<token>/', views.activate, name="activate"),
    path('reset_password/<token>/', views.reset_password, name="reset_password"),
    path('login/forgotpassword/resetpassword/<user_reset>', views.resetpassword, name="resetpassword"),
    path('login/logout/', views.logout),
    path('session/', views.session),




]