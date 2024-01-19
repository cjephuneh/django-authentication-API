from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import Users
from api.authentication import TokenAuthenticationCookie
from api.serializers import ResetEmailSerializer

from typing import Dict


class ResetEmailView(GenericAPIView):
    """
    A view for handling the email reset process.
    It allows an authenticated user to request a reset link
    and updating their email address.

    Allow Methods:
    # POST: Process sending user reset email link.
    """

    authentication_classes = [TokenAuthenticationCookie]
    permission_classes = [IsAuthenticated]
    serializer_class = ResetEmailSerializer

    def send_reset_email(self, user: Users, email: str) -> None:
        """
        Send a reset email with a link for updating
        the user's email address.
        """
        secret_token: str = user.security_token
        reset_url: str = "{}{}".format(
            settings.CLIENT_SITE_URL,
            reverse("reset_email_confirm", kwargs={"token": secret_token}),
        )

        message: str = f"""
        Click the following link to update your new email address. \n{reset_url}
        """
        send_mail(
            "Confirm Your Email Address",
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[email],
            fail_silently=False,
        )
        print(reset_url)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the POST request to initiate the reset email address.

        Return Type -> HttpResponse():
        # A Response indicating the status of sending the reset email link.
        """
        data: Dict = getattr(request, "data", None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        email: str = serializer.validated_data["email_address"]
        user: Users = Users.objects.get(id=request.user.id)
        user.new_email = email
        user.set_security_token
        user.save()
        # sending email to the users new email.
        self.send_reset_email(user=user, email=email)

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _(
                "A reset email link sent to you new email address. Please check."
            ),
        }
        return Response(response_data, status.HTTP_200_OK)


class ResetEmailConfirmView(UpdateAPIView):
    """
    View for confirming the email reset process.

    Allow Methods:
    # PUT: Process user email change confirmed.
    """

    permission_classes = [AllowAny]

    def update(self, request: HttpRequest, token: str = None) -> HttpResponse:
        """
        Handle the update request to confirm the email reset.

        This method checks the validity of the provided security token, updates the
        user's email address, and finalizes the email reset process.

        Return Type -> HttpResponse():
        # A Response indicating the success or failure of the email reset process.
        """
        reset_token = Users.objects.filter(security_token=token).first()

        if reset_token and not reset_token.is_token_expired:
            reset_token.email = reset_token.new_email
            reset_token.security_token = ""
            reset_token.save()

            response_data = {
                "status": status.HTTP_200_OK,
                "message": _("Your email address is change successfully."),
            }
            return Response(response_data, status.HTTP_200_OK)

        return Response(
            {"error": _("Invalid token. Email reset failed.")},
            status.HTTP_404_NOT_FOUND,
        )
