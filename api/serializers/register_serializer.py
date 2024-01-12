from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.validators import password_validator
from api.models import Users


class UserRegisterSerializer(serializers.Serializer):
    """
    A Serializer for user registration.
    """

    username = serializers.CharField(
        label=_("Username"),
        style={"input_type": "text"},
        error_messages={
            "blank": _("Username field is required."),
        },
        validators=[UnicodeUsernameValidator],
        required=True,
    )

    email = serializers.EmailField(
        label=_("Email Address"),
        style={"input_type": "email"},
        error_messages={
            "blank": _("Email field is required."),
        },
        validators=[EmailValidator],
        required=True,
    )

    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        error_messages={
            "blank": _("Password field is required."),
        },
        validators=[password_validator],
        write_only=True,
    )

    def validate(self, attrs):
        """
        Check if a user account with the given username
        or email does not already exist.
        """
        username = attrs.get("username", None)
        email = attrs.get("email", None)

        user_object = Users.objects.filter(Q(username=username) | Q(email=email))

        if user_object.exists():
            raise ValidationError({"error": _("Account already exist.")})

        return attrs

    def create(self, validated_data):
        """
        Create a new user account if it does not already exist.

        Return Type -> Users():
        # Users: The created user instance.
        """

        user = Users.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.send_confirmation_mail()
        return user
