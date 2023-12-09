from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from api.manager import UserManager
from api.models.base import BaseModel


class Users(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    A Custom User model class extending AbstractBaseUser
    and PermissionsMixin.

    Note:
    The purpose of this class is to allow future changes.
    """

    username = models.CharField(
        _("Username"), max_length=50, unique=True, null=False, blank=False
    )
    email = models.EmailField(
        _("Email Address"), max_length=255, unique=True, null=False, blank=False
    )

    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-created_at",)

    def __str__(self):
        return "User >> {}".format(self.username)
