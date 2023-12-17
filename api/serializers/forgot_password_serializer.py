from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from api.models import Users


class ForgotPasswordSerializer(serializers.Serializer):
    """
    A Serializer class for sending reset password link
    to their registered email address.
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

    def validate(self, attrs=None):
        """
        Validate if user email is registered or not.
        """
        email = attrs.get("email_address", None)
        user_email = Users.objects.filter(email=email)

        if not user_email.exists():
            raise NotFound({"error": _("Email address is not registered with us.")})

        return attrs
