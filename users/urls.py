from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from users.forms import UserLoginForm


urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html", authentication_form=UserLoginForm
        ),
        name="login",
    ),
    path("register/", UserCreateView.as_view(), name="register"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("account-setting/", AccountSettingView.as_view(), name="account_setting"),
    path(
        "Customer-portal/",
        StripeCustomerPortalView.as_view(),
        name="customer_portal",
    ),
    path("webhook/", Webhook, name="webhook"),
]
