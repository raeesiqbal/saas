from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import password_validation


class BaseSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = _("Email")
        self.fields["first_name"].widget.attrs["placeholder"] = _("First Name")
        self.fields["first_name"].required = True
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["placeholder"] = _("Last Name")
        self.fields["password1"].widget.attrs[
            "class"
        ] = "form-control form-control-merge"
        self.fields["password1"].widget.attrs["placeholder"] = _("Password")
        self.fields["password2"].widget.attrs[
            "class"
        ] = "form-control form-control-merge"
        self.fields["password2"].widget.attrs["placeholder"] = _("Confirm Password")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"

    username = forms.EmailField()


class BaseEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["first_name"].required = True
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["email"].widget.attrs["readonly"] = True

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
