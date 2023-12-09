from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from typing import Tuple


def set_token_as_cookie(
    response: HttpResponse = None, token: str = None
) -> HttpResponse:
    """
    Set the authentication token as a cookie on the client side.

    Return Type -> HttpResponse():
    # The modified HTTP response object with the token cookie set.

    """
    if (response and token) is not None:
        response.set_cookie(
            key=settings.AUTH_TOKEN_COOKIE["TOKEN_KEY"],
            value=token,
            max_age=settings.AUTH_TOKEN_COOKIE["EXPIRATION"],
            path=settings.AUTH_TOKEN_COOKIE["PATH"],
            secure=settings.AUTH_TOKEN_COOKIE["SECURE"],
            httponly=settings.AUTH_TOKEN_COOKIE["HTTP_ONLY"],
            samesite=settings.AUTH_TOKEN_COOKIE["SAME_SITE"],
        )
        return response
    return None


def delete_token_cookie(request: HttpRequest, response: HttpResponse) -> None:
    """
    Delete the authentication token cookie from the client side.

    Return Type -> None:
    """

    cookie_name: str = settings.AUTH_TOKEN_COOKIE["TOKEN_KEY"]
    get_token_key: str = request.COOKIES.get(cookie_name, None)

    if get_token_key:
        path: str = settings.AUTH_TOKEN_COOKIE["PATH"]
        response.delete_cookie(cookie_name, path=path)
    else:
        return None


class TokenAuthenticationCookie(TokenAuthentication):
    """
    Token Based Authentication with Http-Cookies only.

    This authentication class validates tokens stored
    in client-side cookies.
    """

    model = Token

    def authenticate(self, request: HttpRequest) -> Tuple[str]:
        """
        Authenticate the user based on the token
        stored in cookies.

        Return Type -> Tuple[str]:
        # A tuple containing the authenticated user and token.
        """

        cookie_name: str = settings.AUTH_TOKEN_COOKIE["TOKEN_KEY"]
        get_token_key: str = request.COOKIES.get(cookie_name, None)

        if get_token_key:
            validate_token: tuple(str) = self.authenticate_credentials(get_token_key)
            return validate_token
        return None

    def authenticate_credentials(self, key: str) -> Tuple[str]:
        """
        Validate the provided token key from
        client cookies.

        Return Type -> Tuple[str]:
        # A tuple containing the authenticated user and token.
        """
        try:
            token: Token = self.model.objects.select_related("user").get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed({"error": _("User token is invalid.")})

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": _("Your account is not active or deleted.")}
            )

        return (token.user, token)
