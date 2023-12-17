from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import ChangePasswordSerializer
from api.authentication import TokenAuthenticationCookie


class ChangePasswordView(UpdateAPIView):
    """
    API endpoint for changing user password after login.

    Allow Methods:
    # PUT: Process users data and return a response.
    """

    authentication_classes = [TokenAuthenticationCookie]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the update of user password.

        Return Type -> HttpResponse():
        # HttpResponse: Response indicating the success of password change.
        """
        data = getattr(request, "data", None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "status": status.HTTP_200_OK,
            "message": _("Your new password has been saved."),
        }

        return Response(response_data, status.HTTP_200_OK)
