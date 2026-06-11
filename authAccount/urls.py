from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('otp/', views.otp, name='otp'),
    path('api/signupview/', views.signupview.as_view(), name='signupview'),
    path('api/loginview/', views.loginview.as_view(), name='loginview'),
    path('api/me/', views.meview.as_view(), name='meview'),
    path('api/otpview/', views.otpview.as_view(), name='otpview'),
    path('api/logoutview/', views.logoutview.as_view(), name='logoutview'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
