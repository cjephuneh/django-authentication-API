from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.serializers import UserRegisterSerializer
from api.models import Users

from typing import Dict


class UserRegisterView(CreateAPIView):
    """
    An API endpoint for user registration.

    Allow Methods:
    # POST: Process user registration and return a response.
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def get_response_data(self, data: Dict = None) -> Dict:
        """
        Get the default response data for a successfully
        user registration.

        Return Type -> Dict:
        # dict: The default response data.
        """
        return {
            "status": status.HTTP_201_CREATED,
            "message": _("User register successfully."),
            "data": data,
        }

    def create(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests for user registration.

        Return Type -> HttpResponse():
        # Response: The API response containing the registration status.

        Note:
        Uses the UserRegisterSerializer for registration data validation.
        """
        data = getattr(request, "data", None)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = self.get_response_data(serializer.data)
        return Response(response_data, status.HTTP_201_CREATED)


class UserAccountConfirmView(APIView):
    """
    An API View for confirming a user account registration.
    """

    permission_classes = [AllowAny]

    def get_auth_user(self, token: str = None) -> Users:
        """
        Get authenticated user by their Security token.

        Return Type -> Users():
        # A Users object if exist, otherwise None.
        """
        return Users.objects.filter(security_token=token).first()

    def post(self, token: str = None) -> HttpResponse:
        """
        Handle POST request to confirm a user account.

        Return Type -> HttpResponse():
        # HttpResponse: Response indicating the status of the account confirmation.
        """
        user_token = self.get_auth_user(token=token)

        if user_token and not user_token.is_token_expired():
            user_token.is_active = True
            user_token.security_token = ""
            user_token.save()
            response_data = {
                "status": status.HTTP_200_OK,
                "message": "Your account confirmed successfully.",
            }
            return Response(response_data, status.HTTP_200_OK)

        raise NotFound({"error": _("Invalid token or not accepted.")})
