from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from api.models import Users
from api.validators import password_validator


class ResetPasswordSerializer(serializers.Serializer):
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


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    A Serializer class for confirming reset password
    to the new password.
    """

    new_password = serializers.CharField(
        label=_("New Password"),
        error_messages={
            "blank": _("This field is required."),
        },
        max_length=128,
        required=True,
        validators=[password_validator],
    )
    new_password_confirm = serializers.CharField(
        label=_("Confirm New Password"),
        error_messages={
            "blank": _("This field is required."),
        },
        max_length=128,
        required=True,
        validators=[password_validator],
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            return serializers.ValidationError(
                {"error": "Your passwords field didn't match."}
            )

        return attrs

    def save(self):
        pass
