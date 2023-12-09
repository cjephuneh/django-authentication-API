from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .users import Users


Users = get_user_model()


class UserProfile(BaseModel):
    """
    A Model representing users profile.
    """

    bio = models.CharField(_("Bio"), max_length=200, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=100, null=True, blank=True)
    website = models.URLField(_("Website"), max_length=200, null=True, blank=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="profile")

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
