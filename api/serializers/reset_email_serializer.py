from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from api.models import Users
from api.validators import password_validator


class ResetEmailSerializer(serializers.Serializer):
    """
    A Serializer class for sending reset email link
    to their newly enter email address.
    """

    email_address = serializers.EmailField(
        label=_("Email Address"),
        max_length=128,
        error_messages={
            "blank": _("Email address is required."),
        },
        validators=[EmailValidator],
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate(self, attrs=None):
        """
        Validate if user email is registered or not.
        """
        email = attrs.get("email_address", None)
        user_email = Users.objects.filter(email=email).exclude(id=self.user.id)

        if email == self.user.email:
            raise ValidationError(
                {"error": _("Email is already registered with your account.")}
            )

        if user_email.exists():
            raise ValidationError(
                {"error": _("Email address is already registered with us.")}
            )

        return attrs
