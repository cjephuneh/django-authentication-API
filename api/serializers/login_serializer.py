from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class UserLoginSerializer(serializers.Serializer):
    """
    A Serializer for user login account.
    """

    username = serializers.CharField(
        label=_("Username"),
        style={"input_type": "text"},
        error_messages={
            "blank": _("Username field is required."),
        },
        required=True,
    )

    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        error_messages={
            "blank": _("Password field is required."),
        },
        write_only=True,
    )

    def authenticate_user(self, **credentials):
        """
        Authenticate the user using the provided credentials.
        """
        return authenticate(self.context["request"], **credentials)

    def get_auth_user(self, username: str = None, password: str = None):
        """
        Retrieve and return the authenticated user.
        """
        if (username and password) is not None:
            user = self.authenticate_user(username=username, password=password)
            if user is None:
                raise AuthenticationFailed(
                    {"error": _("Provided credential is incorrect.")}
                )
            if not user.is_active:
                raise AuthenticationFailed(
                    {"error": _("Your account is not activate.")}
                )
            return user
        return None

    def validate(self, attrs):
        """
        Validate the provided username and password, setting
        the authenticated user in attrs.
        """
        username: str = attrs.get("username", None)
        password: str = attrs.get("password", None)

        self.user = self.get_auth_user(username=username, password=password)
        attrs["user"] = self.user
        return attrs
