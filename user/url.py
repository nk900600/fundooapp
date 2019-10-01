from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import include, url


# all the urls are called
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.Registrations.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.Login.as_view()),
    path('login/forgotpassword', views.ForgotPassword.as_view() ,name="resetpassword"),
    path('activate/<token>/', views.activate, name="activate"),
    path('reset_password/<token>/', views.reset_password, name="reset_password"),
    path('login/forgotpassword/resetpassword/<user_reset>', views.ResetPassword.as_view(), name="resetpassword"),
    path('logout/', views.Logout ,name="Logout"),
    path('session/', views.session),
    # path('hello/', views.Hello.as_view(), name ="hello"),


]