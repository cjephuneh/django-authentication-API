from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed

from api.models import Users


class UsernameOrEmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL using either username or email.
    """

    model = Users

    def authenticate(
        self, request: HttpRequest, username: str = None, password: str = None, **kwargs
    ) -> Users:
        """
        Authenticate the user using either username or email.

        Return Type:
        # Users: The authenticated user instance or None if authentication fails.
        """
        if not (username and password):
            return None

        user: Users = self.get_user_model(username=username)

        if user and not user.check_password(password):
            raise AuthenticationFailed(
                {"error": _("The password you enter is incorrect.")}
            )

        return user

    def get_user_model(self, username: str) -> Users:
        """
        Retrieve the user instance using either username or email.

        Return Type -> Users:
        # Users: The user instance or None if the user does not exist.
        """
        try:
            user = self.model.objects.filter(
                Q(username=username) | Q(email=username)
            ).first()

            return user
        except self.model.DoesNotExist:
            return None
