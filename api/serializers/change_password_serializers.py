from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.validators import password_validator


class ChangePasswordSerializer(serializers.Serializer):
    """
    A Serializer class for handling user password change.
    """

    old_password = serializers.CharField(
        label=_("Old Password"),
        max_length=128,
        style={"input_type": "password"},
        error_messages={
            "blank": _("This password field is required."),
        },
        required=True,
    )

    new_password = serializers.CharField(
        label=_("New Password"),
        max_length=128,
        style={"input_type": "password"},
        error_messages={
            "blank": _("This password field is required."),
        },
        required=True,
        validators=[password_validator],
    )

    confirm_new_password = serializers.CharField(
        label=_("Confirm New Password"),
        max_length=128,
        style={"input_type": "password"},
        error_messages={
            "blank": _("This password field is required."),
        },
        required=True,
        validators=[password_validator],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def update_new_password(self, password):
        """
        set the user's new password into the database.
        """
        if self.user:
            self.user.set_password(password)
            self.user.save()

    def validate_old_password(self, password=None):
        """
        Validate the users old password.
        """
        if self.user and not self.user.check_password(password):
            raise ValidationError(
                {"error": _("Your old password was entered incorrectly.")}
            )
        return password

    def validate(self, attrs):
        """
        Validate that the new password and confirmation match.
        """
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise ValidationError(
                {"error": _("Your new password fields didn't match.")}
            )
        return attrs

    def save(self):
        """
        Save the new password by updating the user's password.
        """
        new_password = self.validated_data["new_password"]
        self.update_new_password(new_password)
