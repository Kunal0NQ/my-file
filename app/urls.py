from django.urls import path,include
from .import views

urlpatterns = [
   path("",views.IndexPage,name="index"),
   path("signup/",views.SgPage,name="signup"),
   path("register/",views.RegisterUser,name="register"),
   path("otppage/",views.OTPPage,name="otppage"),
   path("otp/",views.OtpVerify,name="otp"),
   path("login/",views.LoginPage,name="login"),
]