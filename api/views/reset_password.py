from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import Users
from api.serializers import (
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)

from typing import Dict


class ResetPasswordView(GenericAPIView):
    """
    API endpoint for sending reset password link
    for registered user only.

    Allow Methods:
    # POST: Process users registered email and return a response.
    """

    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def get_auth_user(self, email: str = None) -> Users:
        """
        Get a user by email address.

        Return Type -> Users():
        # A Users object if exist, otherwise None.
        """
        return Users.objects.filter(email=email).first()

    def send_reset_email(self, user=None) -> None:
        """
        Send a password reset email to the specified user.
        """
        secret_token: str = default_token_generator.make_token(user)
        reset_url: str = "{}{}".format(
            settings.CLIENT_SITE_URL,
            reverse(
                "reset_password_confirm", kwargs={"uid": user.id, "token": secret_token}
            ),
        )
        send_mail(
            "Reset Password",
            f"Click the following link to reset your password: \n{reset_url}",
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        A Method for handle POST requests for password reset.

        Return Type -> HttpResponse():
        # A Response object with a success message or an error message.
        """
        data: Dict = getattr(request, "data", None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email_address"]
        user = self.get_auth_user(email)

        self.send_reset_email(user=user)

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _("Password reset link has been sent to your email."),
        }

        return Response(response_data, status.HTTP_200_OK)


class ResetPasswordConfirmView(GenericAPIView):
    """
    An API endpoint for confirming the reset password request.

    Allow Methods:
    # POST: Process both password fields and return some response.
    """

    permission_classes = [AllowAny]
    serializer_class = ResetPasswordConfirmSerializer

    def get_auth_user(self, uid: str = None) -> Users:
        """
        Get a user by their ID.

        Return Type -> Users():
        # A Users object if exist, otherwise None.
        """
        return Users.objects.get(id=uid)

    def post(
        self, request: HttpRequest, uid: str, token: str, *args, **kwargs
    ) -> HttpResponse:
        """
        A Method for handle POST request for confirm resetting
        the users password.

        Return Type -> HttpResponse():
        # Response indicating the status of the password reset confirm.
        """
        user: Users = self.get_auth_user(uid=uid)
        secret_token_exist: bool = default_token_generator.check_token(user, token)

        if not user or not secret_token_exist:
            return Response(
                {"error": _("Invalid user or token. Password reset failed.")},
                status.HTTP_404_NOT_FOUND,
            )

        data: Dict = getattr(request, "data", None)
        serializer = self.get_serializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _("Your password has been changed successfully."),
        }

        return Response(response_data, status.HTTP_200_OK)
