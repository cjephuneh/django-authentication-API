from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import Users
from api.authentication import (
    delete_token_cookie,
    TokenAuthenticationCookie,
)

from typing import Dict


class UserLogoutView(APIView):
    """
    An API endpoint for user logout.

    Allow Methods:
    # GET: Logs out the authenticated user and returns a response.
    """

    authentication_classes = [TokenAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get_response_data(self) -> Dict:
        """
        Get the default response data for a successful logout.

        Return Type -> Dict:
        # dict: The default response data.
        """
        return {
            "status": status.HTTP_200_OK,
            "message": _("You logout successfully."),
        }

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for user logout.

        Return Type -> HttpResponse:
        # HttpResponse: The API response containing the logout status.

        Note:
        Deletes the authentication token cookie to log out the user.
        """
        user: Users = getattr(request, "user", None)

        if user is not None:
            response_data: Dict = self.get_response_data()
            response: HttpResponse = Response(response_data, status.HTTP_200_OK)
            delete_token_cookie(request, response)
            return response

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": _("Something wen't wrong."),
            }
        )
