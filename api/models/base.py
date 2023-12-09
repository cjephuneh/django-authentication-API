from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api.utils import get_unique_uuid


class BaseModel(models.Model):
    """
    A BaseModel class for every model in our app.
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=get_unique_uuid,
        editable=False,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.modified_at = now
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
