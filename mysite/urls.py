"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.forms import (
    UserPasswordResetForm,
    UserPasswordChangeForm,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("users.urls", "users"), namespace="users")),
    path("", include(("pages.urls", "pages"), namespace="pages")),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/reset-password/password-reset.html",
            html_email_template_name="users/reset-password/password-reset-email.html",
            form_class=UserPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset-mail/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/reset-password/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/reset-password/password-reset-confirm.html",
            form_class=UserPasswordChangeForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/reset-password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
