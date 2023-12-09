from django.contrib import admin
from api.models import Users, UserProfile


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "created_at", "is_active")
    fields = (
        "username",
        "email",
        "password",
        "created_at",
        "modified_at",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = (
        "created_at",
        "modified_at",
        "last_login",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio", "address", "website")
