from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as DjanoAdmin

# Register your models here.
class UserAdmin(DjanoAdmin):
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "stripe_id",
                    "subscription_id",
                    "subscription_interval",
                    "subscription_amount",
                    "subscribed",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    ordering = ("email",)
    search_fields = ("email",)


admin.site.register(CustomUser, UserAdmin)
