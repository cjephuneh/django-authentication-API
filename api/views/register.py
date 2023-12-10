from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers import UserRegisterSerializer

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
        Get the default response data for a successful
        user registration.

        Return Type -> Dict:
        # dict: The default response data.
        """
        return {
            "status": status.HTTP_201_CREATED,
            "message": {"success": _("User register successfully.")},
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
