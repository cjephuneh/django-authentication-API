from django.urls import path

from api.views import (
    ChangePasswordView,
    ResetPasswordView,
    ResetPasswordConfirmView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserAccountConfirmView,
    ResetEmailView,
    ResetEmailConfirmView,
    UserDetailView,
)

urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="register"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/logout/", UserLogoutView.as_view(), name="logout"),
    path(
        "user/account/confirm/<str:token>/",
        UserAccountConfirmView.as_view(),
        name="confirm_account",
    ),
    path(
        "user/account/reset-password/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "user/account/reset-password/confirm/<str:uid>/<str:token>/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path("user/account/email/reset", ResetEmailView.as_view(), name="reset_email"),
    path(
        "user/account/email/confirm/<str:token>/",
        ResetEmailConfirmView.as_view(),
        name="reset_email_confirm",
    ),
    path(
        "user/account/password/change/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("user/account/profile/", UserDetailView.as_view(), name="user_profile"),
]
