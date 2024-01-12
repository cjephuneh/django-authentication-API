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
    A Serializer for confirming the reset password
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
        """
        Validate that the new password and confirm new
        password field match.
        """

        if not attrs["new_password"] == attrs["new_password_confirm"]:
            raise ValidationError({"error": "Your passwords field did not match."})

        return attrs

    def update(self, instance, validated_data):
        """
        Update the user instance with the new password.
        """
        new_password = validated_data.get("new_password", instance.password)
        instance.set_password(new_password)
        instance.save()
        return instance
