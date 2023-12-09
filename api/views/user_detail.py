from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.authentication import TokenAuthenticationCookie
from api.models import Users
from api.serializers import UserDetailSerializer


class UserDetailView(GenericAPIView):
    """
    API endpoint for retrieving user profile details.
    * Requires token-based authentication.

    Allow Methods:
    # GET: Retrieve and return the user's profile details.
    """

    authentication_classes = [TokenAuthenticationCookie]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        """
        Handle GET requests to retrieve user profile details.

        Returns:
        A JSON response containing user profile details.
        """

        user = getattr(request, "user", None)
        serializer = self.get_serializer(user)

        response_data = {
            "status": status.HTTP_200_OK,
            "message": {"success": _("Profile successfully loaded.")},
            "data": serializer.data,
        }

        return Response(response_data)
