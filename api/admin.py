from django.contrib import admin
from api.models import Users, UserProfile

from typing import Tuple


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = ("username", "email", "created_at", "is_active")
    fields: Tuple[str] = (
        "username",
        "email",
        "password",
        "new_email",
        "security_token",
        "created_at",
        "modified_at",
        "last_login",
        "is_sent",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    readonly_fields: Tuple[str] = (
        "password",
        "is_sent",
        "created_at",
        "modified_at",
        "last_login",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = ("user", "bio", "address", "website")
    fields: Tuple[str] = (
        "user",
        "bio",
        "address",
        "website",
        "created_at",
        "modified_at",
    )
    readonly_fields: Tuple[str] = ("created_at", "modified_at")
