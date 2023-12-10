from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from api.authentication import set_token_as_cookie
from api.serializers import UserLoginSerializer

from typing import Dict


class UserLoginView(GenericAPIView):
    """
    API endpoint for user login.

    Allow Methods:
    # POST: Process user login and return a response.
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def get_response_data(self) -> Dict:
        """
        Get the default response data for a successful login.

        Return Type -> Dict:
        dict: The default response data.
        """
        return {
            "status": status.HTTP_200_OK,
            "message": {"success": _("Login successfully.")},
        }

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests for user login.

        Return Type -> HttpResponse():
        Response: The API response containing the login status.
        """
        data = getattr(request, "data", None)
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        if user is not None:
            token = get_object_or_404(Token.objects.all(), user=user)
            response_data: Dict = self.get_response_data()
            response: HttpResponse = Response(response_data, status.HTTP_200_OK)
            return set_token_as_cookie(response, token)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
