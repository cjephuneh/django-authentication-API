from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import Users
from api.serializers import ForgotPasswordSerializer

from typing import Dict


class ForgotPasswordView(GenericAPIView):
    """
    API endpoint for sending reset password link
    for registered user only.

    Allow Methods:
    # POST: Process users registered email and return a response.
    """

    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def get_auth_user(self, email: str = None) -> Users:
        """
        Get a user by email address.

        Return Type -> Users():
        # A Users object if found, otherwise None.
        """
        return Users.objects.filter(email=email).first()

    def send_reset_email(self, user=None) -> None:
        """
        Send a password reset email to the specified user.
        """
        secret_token: str = default_token_generator.make_token(user)
        reset_url: str = f"{settings.CLIENT_SITE_URL}/reset-password/{secret_token}"

        send_mail(
            "Reset Password",
            f"Click the following link to reset your password: {reset_url}",
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse():
        """
        A Method for handle POST requests for password reset.

        Return Type -> HttpResponse():
        # A Response object with a success message or an error message.
        """
        data = getattr(request, "data", None)
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
