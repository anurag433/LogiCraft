from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = [
        "id",
        "username",
        "email",
        "name",
        "phone_no",
        "role",
        "is_active",
        "is_staff",
    ]

    list_filter = [
        "role",
        "is_active",
        "is_staff",
    ]

    search_fields = [
        "username",
        "email",
        "name",
        "phone_no",
    ]

    ordering = ["id"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            }
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "name",
                    "email",
                    "phone_no",
                )
            }
        ),
        (
            "Role & Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "name",
                    "phone_no",
                    "password1",
                    "password2",
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )